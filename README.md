```markdown
# Detected: SQL Injection Testing Tool

![GitHub](https://img.shields.io/github/license/HackfutSec/Detected)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/HackfutSec/Detected)
![GitHub issues](https://img.shields.io/github/issues/HackfutSec/Detected)
![GitHub stars](https://img.shields.io/github/stars/HackfutSec/Detected)

**Detected** is a powerful and user-friendly tool designed to detect SQL injection vulnerabilities in web applications. It supports both GET and POST requests, custom payloads, cookies for authenticated testing, and generates detailed JSON reports.

---

## Features

- **SQL Injection Detection**: Tests input parameters for SQLi vulnerabilities.
- **GET and POST Support**: Allows testing of forms and URLs.
- **Custom Payloads**: Load payloads from a file or use the built-in library.
- **Cookie Management**: Test authenticated endpoints using cookies.
- **Detailed Reporting**: Generates a JSON report of detected vulnerabilities.
- **Multi-threading**: Tests multiple URLs and parameters simultaneously for improved efficiency.
- **Update Checker**: Notifies users of new versions.

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Python libraries: `requests`, `colorama`, `tqdm`, `bs4`

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/HackfutSec/Detected.git
   cd Detected
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tool:
   ```bash
   python detected.py
   ```

---

## Usage

### Testing a Single URL

1. Run the tool:
   ```bash
   python detected.py
   ```

2. Choose option `1` to test a single URL.
3. Enter the URL, the parameter to test, and choose the method (GET or POST).
4. Use default payloads or load a custom payload file.
5. If needed, provide a cookie file for authenticated testing.

### Testing a File of URLs

1. Run the tool:
   ```bash
   python detected.py
   ```

2. Choose option `2` to test a file of URLs.
3. Enter the path to the file containing URLs, the parameter to test, and choose the method (GET or POST).
4. Use default payloads or load a custom payload file.
5. If needed, provide a cookie file for authenticated testing.

### Reports

Detected vulnerabilities are logged in `vulnerable_urls.txt`. A detailed report is generated in `report.json`.

---

## Examples

### Testing a URL with Default Payloads
```bash
python detected.py
1
http://example.com/page?id=1
id
1
1
n
```

### Testing a File of URLs with Cookies
```bash
python detected.py
2
urls.txt
id
1
1
y
cookies.json
```

---

## Project Structure

```
Detected/
├── detected.py            # Main script
├── requirements.txt       # Python dependencies
├── payloads.txt           # Example payload file
├── cookies.json           # Example cookie file
├── report.json            # Generated report
├── vulnerable_urls.txt    # Detected vulnerable URLs
└── README.md              # Documentation
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Authors

- **HackfutSec** - Lead developer
- **Contributors** - See the list of [contributors](https://github.com/HackfutSec/Detected/contributors).

---

## Acknowledgments

- Thanks to the open-source community for the libraries used in this project.
- Inspired by popular security tools like SQLmap.

---

## Support

For questions or issues, open an [issue](https://github.com/HackfutSec/Detected/issues) on GitHub.

```

---

### Key Points of the README:
1. **Title and Badges**: Shows the project status (version, license, issues, etc.).
2. **Description**: Briefly explains what the tool is and its main features.
3. **Installation**: Provides clear instructions for installing and setting up the tool.
4. **Usage**: Offers practical examples for testing URLs and files.
5. **Project Structure**: Describes the organization of files in the repository.
6. **Contributing**: Encourages contributions and explains how to contribute.
7. **License**: Specifies the project license.
8. **Authors and Acknowledgments**: Recognizes contributors and inspirations.
9. **Support**: Indicates how to get help.
