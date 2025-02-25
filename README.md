# PDF to Markdown Conversion API

## Overview
This Flask-based REST API converts PDF files to Markdown format, extracting both text and images. The service provides a single endpoint that accepts PDF files and returns JSON responses containing the converted content.

## Technical Architecture

### Core Components
- **Web Framework**: Flask
- **PDF Processing**: marker-pdf library
- **Image Handling**: PIL (Python Imaging Library).venv\Scripts\activate
- **File Storage**: Local filesystem with temporary directories

### API Endpoint

#### POST `/convert`
Converts a PDF file to Markdown format.

**Request**:
```http
POST /convert
Content-Type: multipart/form-data
```

**Parameters**:
- `file`: PDF file (required, max size: 16MB)

**Response Format**:
```json
{
  "status": "success",
  "data": {
    "text": "extracted markdown text",
    "images": ["base64_encoded_image1", "base64_encoded_image2"],
    "filename": "original.pdf",
    "filesize": 12345
  }
}
```

**Error Response**:
```json
{
  "error": "error message"
}
```

## Implementation Details

### Security Features
- File size limit: 16MB
- Temporary file cleanup
- Unique conversion directories
- Secure filename handling

### File Processing Flow
1. File upload validation
2. Unique directory creation
3. PDF conversion using marker-pdf
4. Image extraction and base64 encoding
5. Temporary file cleanup

## Setup Instructions

1. Install dependencies:
```sh
pip install flask marker-pdf pillow
```

2. Create required directories:
```sh
mkdir uploads
```

3. Start the server:
```sh
python app.py
```

## Testing

Use the included test script to verify the API:

```sh
python test_api.py
```

## Error Handling

The API handles several error cases:
- Missing file in request
- Empty filename
- File size exceeds limit
- PDF conversion failures
- Image processing errors

Each error returns an appropriate HTTP status code and error message.

## Logging

The application uses Python's built-in logging module with INFO level, capturing:
- File processing events
- Image conversion status
- Error conditions
- Cleanup operations
