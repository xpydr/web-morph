# WebMorph - Image Converter

A full-stack file conversion application focused on high-performance image format conversion. This project demonstrates modern web development practices with a React + Tailwind frontend and a Python FastAPI + Pillow backend.
Currently supports conversion between 20+ image formats with batch processing and instant zip download of converted files.

## Features

### Client (React + Tailwind CSS)
- Clean, responsive user interface
- Drag-and-drop upload zone powered by `react-dropzone`
- Batch file upload support
- Real-time conversion progress feedback
- One-click download of all converted images as a single ZIP file
### Server (FastAPI + Pillow)
- High-performance image processing using Pillow (PIL)
- Comprehensive format support via explicit `FORMAT_MAP`
- Batch conversion with memory-efficient streaming
- Automatic ZIP packaging of results using StreamingResponse
- Dedicated /api/supported-formats endpoint for dynamic frontend format listing
- CORS enabled for seamless local development

## Tech Stack

### Client
- React 18 (Vite recommended)
- Tailwind CSS v4
- TypeScript

### Server
- Python 3.10+
- FastAPI
- Pillow (PIL Fork)
- Uvicorn (ASGI server)

## Quick Start
### Prerequisites
- Node.js ≥ 18
- Python ≥ 3.10
- pnpm
## Installation & Running Locally
1. Clone the repository
```bash
git clone https://github.com/xpdyr/web-morph.git
cd web-morph
```
2. Start the server
```bash
cd server
python -m venv venv
source venv/vin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
3. In a new terminal, start the client
```bash
cd client
pnpm install
pnpm dev
```
4. Open http://localhost:5173
The app will proxy API requests to http://localhost:8000 automatically

## API Endpoints
GET - `/files/supported-formats` - Returns list of supported extensions/formats
POST - `/files/upload` - Upload images & receive converted ZIP

## Contributing
Contributions are welcome. Please open an issue first to discuss major changes.
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push and open a Pull Request

## License
This project is licensed under the MIT License – see the LICENSE file for details.