import os
import zipfile

def create_zip():
    zip_filename = "CampusHub_Final_Submission.zip"
    
    # Exclude these directories/files from the ZIP
    exclude_dirs = {'.git', 'venv', '__pycache__', 'env', 'media', '.venv'}
    exclude_exts = {'.pyc', '.zip', '.sqlite3'}
    exclude_files = {'take_screenshots.py', 'generate_pdf.py', 'create_zip.py', 'temp_report.html', '.env'}
    
    # Files/Dirs that MUST be included based on prompt
    required_dirs = {'accounts', 'api', 'config', 'database', 'docs', 'events', 'registrations', 'report', 'reports', 'screenshots', 'static', 'students', 'templates', 'volunteers', 'documentation'}
    required_files = {'manage.py', 'README.md', 'requirements.txt'}

    print(f"Creating {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            
            for file in files:
                if file in exclude_files:
                    continue
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                
                file_path = os.path.join(root, file)
                
                # Check if it's in a required dir or is a required root file
                rel_path = os.path.relpath(file_path, '.')
                top_level = rel_path.split(os.sep)[0]
                
                if top_level in required_dirs or rel_path in required_files:
                    zipf.write(file_path, arcname=rel_path)

    print(f"Successfully created {zip_filename}")

if __name__ == "__main__":
    create_zip()
