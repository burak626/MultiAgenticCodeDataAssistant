from flask import Flask, render_template, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import glob
from router_agent import router_agent, router_tools
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
import csv_agent

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'csv_uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('generated_files', exist_ok=True)

# Store chat sessions and their memories in memory (in production, use a database)
chat_sessions = {}
chat_memories = {}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        chat_sessions[session['session_id']] = []
    return render_template('index.html')

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file selected'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update the CSV agent with the new file
            import csv_agent
            from langchain_experimental.agents.agent_toolkits import create_csv_agent
            from langchain_openai import ChatOpenAI
            
            csv_agent.csv_executor = create_csv_agent(
                llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
                path=filepath,
                verbose=True,
                allow_dangerous_code=True
            )
            
            # Add upload message to chat history
            session_id = session.get('session_id')
            if session_id in chat_sessions:
                chat_sessions[session_id].append({
                    'type': 'system',
                    'message': f'CSV file "{filename}" uploaded successfully!',
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
            
            return jsonify({'success': True, 'message': f'File {filename} uploaded successfully'})
        else:
            return jsonify({'success': False, 'message': 'Please upload a CSV file'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error uploading file: {str(e)}'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'success': False, 'message': 'Please enter a message'})
        
        # Ensure session exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Add user message to chat history
        chat_sessions[session_id].append({
            'type': 'user',
            'message': user_message,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
        # Get or create session-specific agent executor with memory
        if session_id not in chat_memories:
            chat_memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        
        session_executor = AgentExecutor(
            agent=router_agent,
            tools=router_tools,
            memory=chat_memories[session_id],
            verbose=True
        )
        
        # Get response from router agent
        try:
            response = session_executor.invoke({"input": user_message})
            bot_response = response.get('output', 'Sorry, I could not process your request.')
            
            # Determine which agent was used
            agent_name = "AI Assistant"
            if "python" in user_message.lower() or "code" in user_message.lower() or "qr" in user_message.lower():
                agent_name = "Python Agent"
            elif "csv" in user_message.lower() or "data" in user_message.lower() or "episode" in user_message.lower():
                agent_name = "CSV Agent"
                
        except Exception as e:
            bot_response = f"Error processing request: {str(e)}"
            agent_name = "AI Assistant"
        
        # Check if QR code was generated and add image and download link
        download_url = None
        image_url = None
        if "qr_code_" in bot_response and ".png" in bot_response:
            # Extract filename from response
            import re
            filename_match = re.search(r'qr_code_\w+\.png', bot_response)
            if filename_match:
                filename = filename_match.group()
                download_url = f'/download/{filename}'
                image_url = f'/image/{filename}'
        
        # Add bot response to chat history
        bot_message = {
            'type': 'bot',
            'message': bot_response,
            'agent_name': agent_name,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        if download_url:
            bot_message['download_url'] = download_url
        if image_url:
            bot_message['image_url'] = image_url
            
        chat_sessions[session_id].append(bot_message)
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'chat_history': chat_sessions[session_id]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/get_chat_history')
def get_chat_history():
    # Ensure session exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        chat_sessions[session['session_id']] = []
    
    session_id = session['session_id']
    if session_id in chat_sessions:
        return jsonify({'chat_history': chat_sessions[session_id]})
    return jsonify({'chat_history': []})

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Clear the chat history"""
    # Ensure session exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']
    chat_sessions[session_id] = []
    
    # Clear the memory for this session
    if session_id in chat_memories:
        chat_memories[session_id].clear()
    
    return jsonify({'success': True, 'message': 'Chat history cleared'})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join('generated_files', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/image/<filename>')
def serve_image(filename):
    try:
        file_path = os.path.join('generated_files', filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_generated_files')
def list_generated_files():
    try:
        files = []
        for file_path in glob.glob('generated_files/*'):
            filename = os.path.basename(file_path)
            files.append({
                'name': filename,
                'download_url': f'/download/{filename}'
            })
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)