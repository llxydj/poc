#!/usr/bin/env python3
"""
Setup Verification Script for BAYANIHUB POC
Checks if all components are properly installed and configured.
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"  ✅ {package_name} installed")
        return True
    except ImportError:
        print(f"  ❌ {package_name} NOT installed")
        return False

def check_required_packages():
    """Check all required packages"""
    print("\nChecking required packages...")
    packages = [
        ("Flask", "flask"),
        ("Flask-CORS", "flask_cors"),
        ("Streamlit", "streamlit"),
        ("scikit-learn", "sklearn"),
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
        ("Plotly", "plotly"),
        ("Requests", "requests"),
        ("Joblib", "joblib"),
    ]
    
    all_ok = True
    for name, import_name in packages:
        if not check_package(name, import_name):
            all_ok = False
    
    # Check NumPy version specifically
    try:
        import numpy
        version = numpy.__version__
        major, minor = map(int, version.split('.')[:2])
        if major == 1 and minor >= 25:
            print(f"  ✅ NumPy version {version} (OK - >= 1.25.2)")
        else:
            print(f"  ⚠️  NumPy version {version} (May need >= 1.25.2)")
    except:
        pass
    
    return all_ok

def check_project_structure():
    """Check project structure"""
    print("\nChecking project structure...")
    required_dirs = [
        "hub",
        "dashboard",
        "suc_simulators",
        "anomaly"
    ]
    
    required_files = [
        "hub/app.py",
        "hub/storage.py",
        "hub/correlation.py",
        "dashboard/dashboard.py",
        "suc_simulators/suc_a.py",
        "suc_simulators/suc_b.py",
        "anomaly/detector.py",
        "requirements.txt"
    ]
    
    all_ok = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"  ✅ Directory '{dir_name}' exists")
        else:
            print(f"  ❌ Directory '{dir_name}' missing")
            all_ok = False
    
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"  ✅ File '{file_name}' exists")
        else:
            print(f"  ❌ File '{file_name}' missing")
            all_ok = False
    
    return all_ok

def check_database():
    """Check database setup"""
    print("\nChecking database setup...")
    db_path = os.path.join("hub", "bayanihub.db")
    
    if os.path.isfile(db_path):
        print(f"  ✅ Database file exists: {db_path}")
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                print(f"  ✅ Database has {len(tables)} table(s)")
                for table in tables:
                    print(f"     - {table[0]}")
            else:
                print(f"  ⚠️  Database exists but has no tables")
            conn.close()
        except Exception as e:
            print(f"  ⚠️  Could not read database: {e}")
    else:
        print(f"  ℹ️  Database will be created automatically when hub starts")
        print(f"     Expected location: {db_path}")
    
    return True

def check_model_file():
    """Check ML model file"""
    print("\nChecking ML model...")
    model_path = "if_model.joblib"
    
    if os.path.isfile(model_path):
        print(f"  ✅ Model file exists: {model_path}")
    else:
        print(f"  ℹ️  Model will be created automatically on first run")
        print(f"     Expected location: {model_path}")
    
    return True

def check_ports():
    """Check if ports are available"""
    print("\nChecking ports...")
    import socket
    
    ports = {
        5000: "Hub API",
        8501: "Dashboard"
    }
    
    all_ok = True
    for port, name in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result != 0:
            print(f"  ✅ Port {port} ({name}) is available")
        else:
            print(f"  ⚠️  Port {port} ({name}) is in use")
            print(f"     You may need to stop the service using this port")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("BAYANIHUB POC - Setup Verification")
    print("=" * 60)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Required Packages", check_required_packages()))
    results.append(("Project Structure", check_project_structure()))
    results.append(("Database Setup", check_database()))
    results.append(("ML Model", check_model_file()))
    results.append(("Port Availability", check_ports()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! You're ready to run the system.")
        print("\nNext steps:")
        print("1. Start hub: cd hub && python app.py")
        print("2. Start dashboard: cd dashboard && streamlit run dashboard.py")
        print("3. Start SUC simulators: python suc_simulators/suc_a.py")
        print("4. Start SUC simulators: python suc_simulators/suc_b.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Fix NumPy version: pip install numpy==1.26.4")
        print("- Check project structure")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())

