



https://github.com/user-attachments/assets/a82ddad9-67dd-43fb-a2de-3e5f5641d08e


_______________________________________________________________________________________________________________________________
# AI-Powered Resume Builder 🚀  

## 📌 Overview  

The **AI-Powered Resume Builder** is a web application that leverages artificial intelligence to help users generate, enhance, and format resumes effortlessly. It integrates AI-driven text generation, smart content recommendations, and automated resume formatting to simplify the resume-building process.  

## 🛠️ Tech Stack  

### **Frontend**  
- **Next.js** (React Framework)  
- **Tailwind CSS** (UI Styling)  
- **html-to-image** (PDF Export)  

### **Backend**  
- **FastAPI** (AI API & Backend Services)  
- **Supabase** (Authentication & Database)  
- **Render** (Backend Deployment)  

### **AI Integration**  
- **Hugging Face API** (Open-source AI Model)  
- **distilgpt2** (Text Generation & Resume Optimization)  

### **Deployment**  
- **Vercel** (Frontend Hosting)  
- **Supabase Storage** (Resume File Storage)  

## ✨ AI-Powered Features  

✅ **Auto-Generate Resume Content** – AI generates job descriptions, summaries, and skills from minimal user input.  
✅ **Smart Resume Recommendations** – AI suggests missing sections or improvements.  

## 🚀 Installation & Setup  

1. **Clone the repository**  
   ```bash
   https://github.com/jostan30/ai-resume-builder-backend.git
   cd ai-resume-builder-backend
   ```

2. **Install dependencies**  
   ```bash
   npm install
   ```

3. **Run the backend (FastAPI)**  
   ```bash
   uvicorn main:app --reload
   ```

4. **Environment Variables**  
   Set up `.env` file for API keys (OpenAI, Hugging Face, Supabase, etc.).
   ```bash
   ENVIRONMENT=development
   # Model selectin 
   DEFAULT_MODEL=facebook/bart-large-cnn
   #Add any API keys or secrets here
   #HF_API_TOKEN=your_huggingface_token_if_needed
   ```



## 📌 Next Steps  

- Choose an **AI model** (`GPT-3.5-turbo` or `BLOOM`, I have used `distilgpt2`).  
- Set up the **AI API using FastAPI**.   

Backend isnt deployed so ai-features wont work ,
Check out frontend code 
`https://github.com/jostan30/ai-resume-builder`
