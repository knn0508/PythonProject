from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import os
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import mimetypes

# Import our enhanced models and configuration
try:
    from models import EnhancedKnowledgeBase, UserManager, EnhancedAIAssistant
    from file_manager import FileManager
    from config import Config
    IMPORTS_SUCCESS = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_SUCCESS = False
    # Fallback configuration
    class Config:
        SECRET_KEY = 'fallback-secret-key'
        GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
        DEBUG = False
        HOST = '0.0.0.0'
        PORT = 5000

import sqlite3

app = Flask(__name__)
app.config.from_object(Config)

def init_app():
    """Initialize application for serverless environment"""
    # Create necessary directories
    try:
        os.makedirs('/tmp/temp', exist_ok=True)
        os.makedirs('/tmp/documents', exist_ok=True)
    except:
        os.makedirs('temp', exist_ok=True)
        os.makedirs('documents', exist_ok=True)
    
    # Initialize components with better error handling
    global file_manager, knowledge_base, user_manager, ai_assistant
    
    if IMPORTS_SUCCESS:
        try:
            # Initialize UserManager first
            print("Initializing UserManager...")
            user_manager = UserManager()
            user_manager.initialize_db()  # Force database creation
            print("✅ UserManager initialized")
            
            # Initialize FileManager
            print("Initializing FileManager...")
            file_manager = FileManager()
            print("✅ FileManager initialized")
            
            # Initialize KnowledgeBase
            print("Initializing KnowledgeBase...")
            knowledge_base = EnhancedKnowledgeBase(file_manager)
            print("✅ KnowledgeBase initialized")
            
            # Initialize AI Assistant
            print("Initializing AI Assistant...")
            ai_assistant = EnhancedAIAssistant(knowledge_base, Config.GEMINI_API_KEY)
            print("✅ AI Assistant initialized")
            
            print("🎉 All components initialized successfully!")
            
        except Exception as e:
            print(f"❌ Component initialization error: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            
            # Try to initialize at least the basic user manager
            try:
                user_manager = UserManager()
                user_manager.initialize_db()
                print("✅ Basic UserManager fallback initialized")
            except:
                user_manager = None
                print("❌ Even basic UserManager failed")
            
            file_manager = None
            knowledge_base = None
            ai_assistant = None
    else:
        file_manager = None
        knowledge_base = None
        user_manager = None
        ai_assistant = None
        print("⚠️ Running in fallback mode due to import errors")

# Initialize for serverless
init_app()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({'error': 'Admin icazəsi tələb olunur'}), 403
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    # Check if components are loaded
    try:
        if IMPORTS_SUCCESS and user_manager is not None:
            # Full app mode - redirect to proper flow
            if 'user_id' in session:
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))
    except:
        pass
    
    # Fallback mode if components not loaded
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Onboarding System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .status { text-align: center; padding: 20px; background: #e7f3ff; border-radius: 5px; margin: 20px 0; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; text-decoration: none; display: inline-block; }
            .error { background: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AI Onboarding System</h1>
            <div class="status">
                <h3>⚠️ System Loading...</h3>
                <p>The application components are initializing.</p>
                <p><strong>Time:</strong> ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
            </div>
            <div class="error">
                <p><strong>Debug Info:</strong></p>
                <p>IMPORTS_SUCCESS: ''' + str(IMPORTS_SUCCESS) + '''</p>
                <p>user_manager: ''' + str(user_manager is not None) + '''</p>
            </div>
            <div style="text-align: center;">
                <a href="/health" class="btn">Health Check</a>
                <a href="/api/status" class="btn">API Status</a>
                <a href="/login" class="btn">Try Login</a>
            </div>
        </div>
    </body>
    </html>
    '''


@app.route('/health')
def health_check():
    """Health check endpoint for Vercel"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/status')
def api_status():
    """API status endpoint"""
    try:
        # Test if components are loaded
        if not IMPORTS_SUCCESS:
            return jsonify({
                'status': 'import_failed',
                'message': 'Import errors occurred',
                'imports_success': False,
                'user_manager': False,
                'timestamp': datetime.now().isoformat()
            })
        
        # Check each component
        component_status = {
            'user_manager': user_manager is not None,
            'file_manager': file_manager is not None,
            'knowledge_base': knowledge_base is not None,
            'ai_assistant': ai_assistant is not None
        }
        
        if user_manager:
            try:
                user_manager.initialize_db()
                db_status = 'connected'
            except Exception as e:
                db_status = f'error: {str(e)}'
        else:
            db_status = 'not_initialized'
        
        return jsonify({
            'status': 'ok' if all(component_status.values()) else 'partial',
            'database': db_status,
            'components': component_status,
            'imports_success': IMPORTS_SUCCESS,
            'ai_model': 'gemini-2.5-flash' if ai_assistant else 'not_loaded',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user_manager is available
    if user_manager is None:
        if request.method == 'POST':
            return jsonify({
                'success': False, 
                'message': 'Sistem hələ başlamır. Zəhmət olmasa bir az gözləyin.'
            })
        else:
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Sistem Yüklənir</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; text-align: center; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
                    .loading { color: #007bff; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔄 Sistem Yüklənir</h1>
                    <p class="loading">AI Onboarding sistemi hazırlanır. Zəhmət olmasa bir neçə saniyə gözləyin...</p>
                    <p><a href="/">Ana səhifəyə qayıt</a></p>
                    <script>
                        setTimeout(function() {
                            window.location.reload();
                        }, 5000);
                    </script>
                </div>
            </body>
            </html>
            '''
    
    if request.method == 'POST':
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            user = user_manager.authenticate(username, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['name'] = user['name']
                session['role'] = user['role']
                return jsonify({'success': True, 'user': user})
            else:
                return jsonify({'success': False, 'message': 'Yanlış istifadəçi adı və ya şifrə!'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Xəta: {str(e)}'})

    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    if user_manager.create_user(username, password, name, role):
        user = user_manager.authenticate(username, password)
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['name'] = user['name']
        session['role'] = user['role']
        return jsonify({'success': True, 'user': user})
    else:
        return jsonify({'success': False, 'message': 'Bu istifadəçi adı artıq mövcuddur!'})


@app.route('/dashboard')
@login_required
def dashboard():
    user_info = {
        'id': session['user_id'],
        'username': session['username'],
        'name': session['name'],
        'role': session['role']
    }

    # Get recent documents for dashboard
    recent_files = file_manager.list_files()[:5]  # Last 5 files

    return render_template('dashboard.html', user=user_info, recent_files=recent_files)


@app.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()

        if not message:
            return jsonify({'error': 'Boş mesaj göndərilə bilməz'}), 400

        user_info = {
            'id': session['user_id'],
            'username': session['username'],
            'name': session['name'],
            'role': session['role']
        }

        # Generate AI response with enhanced capabilities
        response = ai_assistant.generate_enhanced_response(message, user_info)

        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({
            'success': False,
            'error': 'Texniki problem yarandı. Zəhmət olmasa yenidən cəhd edin.'
        }), 500


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Fayl seçilməyib'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Fayl seçilməyib'}), 400

        # Get additional metadata
        category = request.form.get('category', 'Ümumi')
        description = request.form.get('description', '')
        tags = request.form.get('tags', '').split(',') if request.form.get('tags') else []

        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join('temp', filename)
        os.makedirs('temp', exist_ok=True)
        file.save(temp_path)

        # Process with file manager
        result = file_manager.upload_file(
            temp_path,
            category=category,
            tags=tags,
            description=description
        )

        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        if result.get('success'):
            return jsonify({
                'success': True,
                'message': f'{filename} uğurla yükləndi',
                'file_info': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Fayl yüklənə bilmədi')
            }), 500

    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({
            'success': False,
            'error': 'Fayl yükləmə zamanı xəta baş verdi'
        }), 500


@app.route('/files')
@login_required
def list_files():
    """List all uploaded files"""
    try:
        category = request.args.get('category')
        files = file_manager.list_files(category=category)

        return jsonify({
            'success': True,
            'files': files
        })
    except Exception as e:
        print(f"List files error: {e}")
        return jsonify({
            'success': False,
            'error': 'Faylları yükləmə zamanı xəta baş verdi'
        }), 500


@app.route('/files/<file_id>')
@login_required
def get_file_content(file_id):
    """Get file content by ID"""
    try:
        chunk_index = request.args.get('chunk', type=int)
        content = file_manager.get_file_content(file_id, chunk_index)

        if content.get('error'):
            return jsonify({'error': content['error']}), 404

        return jsonify({
            'success': True,
            'content': content
        })
    except Exception as e:
        print(f"Get file error: {e}")
        return jsonify({
            'success': False,
            'error': 'Fayl məzmunu yüklənə bilmədi'
        }), 500


@app.route('/search-files')
@login_required
def search_files():
    """Search through uploaded files"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category')

        if not query:
            return jsonify({'error': 'Axtarış sorğusu tələb olunur'}), 400

        results = file_manager.search_files(query, category=category)

        return jsonify({
            'success': True,
            'results': results,
            'query': query
        })
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({
            'success': False,
            'error': 'Axtarış zamanı xəta baş verdi'
        }), 500


@app.route('/bulk-upload', methods=['POST'])
@admin_required
def bulk_upload():
    """Bulk upload files from directory (Admin only)"""
    try:
        data = request.json
        directory_path = data.get('directory_path')
        category = data.get('category', 'Bulk Upload')

        if not directory_path:
            return jsonify({'error': 'Directory path tələb olunur'}), 400

        if not os.path.exists(directory_path):
            return jsonify({'error': 'Directory tapılmadı'}), 400

        result = file_manager.bulk_upload(directory_path, category=category)

        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        print(f"Bulk upload error: {e}")
        return jsonify({
            'success': False,
            'error': 'Bulk upload zamanı xəta baş verdi'
        }), 500


@app.route('/file-stats')
@login_required
def file_stats():
    """Get file statistics"""
    try:
        files = file_manager.list_files()

        stats = {
            'total_files': len(files),
            'file_types': {},
            'categories': {},
            'total_size': 0
        }

        for file_info in files:
            # Count by file type
            file_type = file_info['file_type']
            stats['file_types'][file_type] = stats['file_types'].get(file_type, 0) + 1

            # Count by category
            category = file_info.get('category', 'Uncategorized')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1

            # Sum file sizes
            stats['total_size'] += file_info.get('file_size', 0)

        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        print(f"Stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Statistikalar yüklənə bilmədi'
        }), 500


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/knowledge-search')
@login_required
def knowledge_search():
    """Enhanced knowledge search including documents"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Axtarış sorğusu tələb olunur'}), 400

        results = knowledge_base.search(query)

        return jsonify({
            'success': True,
            'results': results,
            'query': query
        })
    except Exception as e:
        print(f"Knowledge search error: {e}")
        return jsonify({
            'success': False,
            'error': 'Bilik bazası axtarışında xəta baş verdi'
        }), 500


@app.route('/documents')
@login_required
def documents_page():
    """Documents management page"""
    user_info = {
        'id': session['user_id'],
        'username': session['username'],
        'name': session['name'],
        'role': session['role']
    }
    return render_template('documents.html', user=user_info)


# Add these routes to your existing app.py file

@app.route('/download/<file_id>')
@login_required
def download_file(file_id):
    """Download a file by its ID"""
    try:
        # Get file info from database
        conn = sqlite3.connect(file_manager.db_path)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT filename, file_path, file_type
                       FROM files
                       WHERE id = ?
                       ''', (file_id,))

        file_info = cursor.fetchone()
        conn.close()

        if not file_info:
            return jsonify({'error': 'File not found'}), 404

        filename, file_path, file_type = file_info

        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({'error': 'Physical file not found'}), 404

        # Send file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetypes.guess_type(filename)[0]
        )

    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': 'Download failed'}), 500


@app.route('/download-all')
@admin_required
def download_all_files():
    """Download all files as ZIP (Admin only)"""
    try:
        import zipfile
        from io import BytesIO

        # Create ZIP in memory
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Get all files
            files = file_manager.list_files()

            for file_info in files:
                file_path = None

                # Get file path from database
                conn = sqlite3.connect(file_manager.db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT file_path FROM files WHERE id = ?', (file_info['file_id'],))
                result = cursor.fetchone()
                conn.close()

                if result and os.path.exists(result[0]):
                    file_path = result[0]
                    # Add file to ZIP with category folder structure
                    category = file_info.get('category', 'Uncategorized')
                    zip_path = f"{category}/{file_info['filename']}"
                    zip_file.write(file_path, zip_path)

        zip_buffer.seek(0)

        return send_file(
            BytesIO(zip_buffer.read()),
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'nazirlik_documents_{datetime.now().strftime("%Y%m%d")}.zip'
        )

    except Exception as e:
        print(f"Download all error: {e}")
        return jsonify({'error': 'ZIP creation failed'}), 500


@app.route('/files/<file_id>/info')
@login_required
def get_file_info(file_id):
    """Get detailed file information"""
    try:
        conn = sqlite3.connect(file_manager.db_path)
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT f.*, COUNT(c.id) as chunk_count
                       FROM files f
                                LEFT JOIN chunks c ON f.id = c.file_id
                       WHERE f.id = ?
                       GROUP BY f.id
                       ''', (file_id,))

        file_data = cursor.fetchone()
        conn.close()

        if not file_data:
            return jsonify({'error': 'File not found'}), 404

        file_info = {
            'file_id': file_data[0],
            'filename': file_data[1],
            'original_name': file_data[2],
            'file_type': file_data[4],
            'file_size': file_data[5],
            'upload_date': file_data[7],
            'category': file_data[9],
            'description': file_data[11],
            'chunk_count': file_data[14],
            'download_url': url_for('download_file', file_id=file_id)
        }

        return jsonify({
            'success': True,
            'file_info': file_info
        })

    except Exception as e:
        print(f"File info error: {e}")
        return jsonify({'error': 'Could not get file info'}), 500


@app.route('/export-data')
@admin_required
def export_data():
    """Export all data including files and database (Admin only)"""
    try:
        import zipfile
        from io import BytesIO
        import json

        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:

            # 1. Add all documents
            files = file_manager.list_files()
            for file_info in files:
                conn = sqlite3.connect(file_manager.db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT file_path FROM files WHERE id = ?', (file_info['file_id'],))
                result = cursor.fetchone()
                conn.close()

                if result and os.path.exists(result[0]):
                    category = file_info.get('category', 'Uncategorized')
                    zip_path = f"documents/{category}/{file_info['filename']}"
                    zip_file.write(result[0], zip_path)

            # 2. Add databases
            if os.path.exists('users.db'):
                zip_file.write('users.db', 'database/users.db')
            if os.path.exists('file_index.db'):
                zip_file.write('file_index.db', 'database/file_index.db')

            # 3. Add file metadata as JSON
            metadata = {
                'export_date': datetime.now().isoformat(),
                'total_files': len(files),
                'files': files
            }
            zip_file.writestr('metadata.json', json.dumps(metadata, ensure_ascii=False, indent=2))

        zip_buffer.seek(0)

        return send_file(
            BytesIO(zip_buffer.read()),
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'nazirlik_full_export_{datetime.now().strftime("%Y%m%d_%H%M")}.zip'
        )

    except Exception as e:
        print(f"Export error: {e}")
        return jsonify({'error': 'Export failed'}), 500

@app.route('/files-manager')
@login_required
def files_manager():
    """File management page"""
    user_info = {
        'id': session['user_id'],
        'username': session['username'],
        'name': session['name'],
        'role': session['role']
    }
    return render_template('files.html', user=user_info)

# For local development only
if __name__ == '__main__':
    print("🚀 Enhanced AI Onboarding System Starting...")
    print("📧 Demo Accounts:")
    print("   Admin: admin / admin123")
    print("   Minister: nazir / nazir123")
    print("   Analyst: analitik / data123")
    print("🤖 Gemini 2.5 Flash AI Model: Ready")
    print("📁 File Management System: Ready")
    print("🔍 Document Search: Ready")
    print(f"🌐 Server: http://{Config.HOST}:{Config.PORT}")

    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)