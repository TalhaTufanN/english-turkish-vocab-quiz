from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import random
from typing import Dict, Any

from src.read_words_from_txt import read_words_from_txt
from src.translate_words import translate_words
from src.create_word_list_pdf import create_word_list_pdf
from src.generate_choices import generate_choices
from src.create_quiz_pdf import create_pdf

app = FastAPI(title="TestMaker UI", description="Modern UI for the TestMaker Application")

# Mount the static directory
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS for frontend requests if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.post("/api/process")
async def process_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"File uploaded: {file.filename}")
        
        # Read words
        words = read_words_from_txt(temp_file_path)
        if len(words) < 50:
            raise HTTPException(status_code=400, detail="The file must contain at least 50 words.")
            
        # Translate words
        translations = translate_words(words)
        
        # Generate Word List PDF
        word_list_pdf_path = create_word_list_pdf(translations)
        
        # Select 50 words for the quiz and generate choices
        test_words = random.sample(list(translations.keys()), 50)
        questions = {word: generate_choices(translations[word], list(translations.values())) for word in test_words}
        
        # Generate Quiz PDF
        quiz_pdf_path = create_pdf(questions)
        
        # Return the paths so the frontend can download them
        # Convert to relative paths that can be served
        return {
            "success": True,
            "word_list_url": f"/api/download/{os.path.basename(word_list_pdf_path)}?type=words",
            "quiz_url": f"/api/download/{os.path.basename(quiz_pdf_path)}?type=quizzes",
            "message": "Files processed successfully!"
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary uploaded file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/api/download/{filename}")
async def download_file(filename: str, type: str):
    # type must be 'words' or 'quizzes'
    if type not in ["words", "quizzes"]:
        raise HTTPException(status_code=400, detail="Invalid file type requested")
        
    file_path = os.path.join(type, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf", filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
