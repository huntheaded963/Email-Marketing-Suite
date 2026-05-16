"""
Multi-Language Support for Email Marketing Tools
دعم متعدد اللغات لأدوات التسويق عبر البريد الإلكتروني
"""

import subprocess
import os
import json
from typing import Dict, List, Optional
import tempfile

class MultiLanguageBridge:
    """Bridge to support multiple programming languages"""
    
    def __init__(self):
        self.supported_languages = {
            'python': {'ext': '.py', 'command': 'python3'},
            'javascript': {'ext': '.js', 'command': 'node'},
            'java': {'ext': '.java', 'command': 'javac'},
            'go': {'ext': '.go', 'command': 'go'},
            'rust': {'ext': '.rs', 'command': 'rustc'},
            'php': {'ext': '.php', 'command': 'php'},
            'ruby': {'ext': '.rb', 'command': 'ruby'},
            'c': {'ext': '.c', 'command': 'gcc'},
            'cpp': {'ext': '.cpp', 'command': 'g++'},
            'swift': {'ext': '.swift', 'command': 'swift'},
            'kotlin': {'ext': '.kt', 'command': 'kotlinc'},
            'r': {'ext': '.r', 'command': 'Rscript'},
            'perl': {'ext': '.pl', 'command': 'perl'},
            'lua': {'ext': '.lua', 'command': 'lua'},
            'scala': {'ext': '.scala', 'command': 'scala'},
            'dart': {'ext': '.dart', 'command': 'dart'},
            'typescript': {'ext': '.ts', 'command': 'ts-node'},
            'shell': {'ext': '.sh', 'command': 'bash'},
            'powershell': {'ext': '.ps1', 'command': 'powershell'}
        }
    
    def execute_code(self, language: str, code: str, input_data: Dict = None) -> Dict:
        """Execute code in specified language"""
        if language.lower() not in self.supported_languages:
            return {'status': 'error', 'message': f'Language {language} not supported'}
        
        lang_info = self.supported_languages[language.lower()]
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix=lang_info['ext'],
                delete=False
            ) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute based on language
            if language.lower() == 'java':
                return self._execute_java(temp_file, input_data)
            elif language.lower() == 'go':
                return self._execute_go(temp_file, input_data)
            elif language.lower() == 'rust':
                return self._execute_rust(temp_file, input_data)
            elif language.lower() == 'c' or language.lower() == 'cpp':
                return self._execute_c(temp_file, language.lower(), input_data)
            else:
                return self._execute_script(lang_info['command'], temp_file, input_data)
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        finally:
            # Cleanup
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def _execute_script(self, command: str, file_path: str, input_data: Dict = None) -> Dict:
        """Execute script-based language"""
        try:
            if input_data:
                input_json = json.dumps(input_data)
                result = subprocess.run(
                    [command, file_path],
                    input=input_json,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                result = subprocess.run(
                    [command, file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            return {
                'status': 'success' if result.returncode == 0 else 'error',
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'status': 'error', 'message': 'Execution timeout'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _execute_java(self, file_path: str, input_data: Dict = None) -> Dict:
        """Execute Java code"""
        try:
            # Compile
            compile_result = subprocess.run(
                ['javac', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile_result.returncode != 0:
                return {
                    'status': 'error',
                    'message': 'Compilation failed',
                    'error': compile_result.stderr
                }
            
            # Execute
            class_file = file_path.replace('.java', '.class')
            class_name = os.path.basename(class_file).replace('.class', '')
            class_dir = os.path.dirname(class_file)
            
            result = subprocess.run(
                ['java', '-cp', class_dir, class_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Cleanup
            try:
                os.unlink(class_file)
            except:
                pass
            
            return {
                'status': 'success' if result.returncode == 0 else 'error',
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _execute_go(self, file_path: str, input_data: Dict = None) -> Dict:
        """Execute Go code"""
        try:
            result = subprocess.run(
                ['go', 'run', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'status': 'success' if result.returncode == 0 else 'error',
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _execute_rust(self, file_path: str, input_data: Dict = None) -> Dict:
        """Execute Rust code"""
        try:
            # Compile and run
            result = subprocess.run(
                ['rustc', file_path, '-o', file_path + '.exe'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {
                    'status': 'error',
                    'message': 'Compilation failed',
                    'error': result.stderr
                }
            
            # Execute
            exec_result = subprocess.run(
                [file_path + '.exe'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Cleanup
            try:
                os.unlink(file_path + '.exe')
            except:
                pass
            
            return {
                'status': 'success' if exec_result.returncode == 0 else 'error',
                'output': exec_result.stdout,
                'error': exec_result.stderr
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _execute_c(self, file_path: str, lang: str, input_data: Dict = None) -> Dict:
        """Execute C/C++ code"""
        try:
            compiler = 'gcc' if lang == 'c' else 'g++'
            output_file = file_path + '.exe'
            
            # Compile
            compile_result = subprocess.run(
                [compiler, file_path, '-o', output_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile_result.returncode != 0:
                return {
                    'status': 'error',
                    'message': 'Compilation failed',
                    'error': compile_result.stderr
                }
            
            # Execute
            exec_result = subprocess.run(
                [output_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Cleanup
            try:
                os.unlink(output_file)
            except:
                pass
            
            return {
                'status': 'success' if exec_result.returncode == 0 else 'error',
                'output': exec_result.stdout,
                'error': exec_result.stderr
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.supported_languages.keys())
    
    def check_language_available(self, language: str) -> bool:
        """Check if language runtime is available"""
        lang_info = self.supported_languages.get(language.lower())
        if not lang_info:
            return False
        
        try:
            result = subprocess.run(
                [lang_info['command'], '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

