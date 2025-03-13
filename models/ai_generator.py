from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self):
        # Use a better model for text generation
        self.model_name = "gpt2-medium"  # Free and available on Hugging Face
        self.device = 0 if torch.cuda.is_available() else -1
        
        logger.info(f"Loading model: {self.model_name}")
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Initialize text generation pipeline
            self.generator = pipeline(
                "text-generation", 
                model=self.model, 
                tokenizer=self.tokenizer,
                device=self.device
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def generate_summary(self, job_title):
        """Generate a professional summary for a resume based on job title"""
        # Create a more structured prompt with clear markers
        prompt = f"""TASK: Write a professional resume summary.
JOB TITLE: {job_title}
INSTRUCTIONS: The summary should be in first person, be around 50 words, and highlight key qualifications. Write as a single paragraph.
SUMMARY: I am a skilled {job_title} with experience in"""
        try:
            # Generate text
            result = self.generator(
                prompt,
                max_length=250,  # Reduced to get more concise results
                min_length=150,   # Ensure we get something substantial
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1,
                no_repeat_ngram_size=2
            )
            
            # Extract generated text
            generated_text = result[0]["generated_text"]
            
            # Extract just the summary part
           # Extract the complete text after "SUMMARY: "
            summary_pattern = r"SUMMARY:\s*(.*?)(?:ENDMARKER|$)"
            summary_match = re.search(summary_pattern, generated_text, re.DOTALL)
            
            if summary_match:
                summary = summary_match.group(1).strip()
            else:
                # Extract anything after "SUMMARY:"
                parts = generated_text.split("SUMMARY:")
                if len(parts) > 1:
                    summary = parts[1].strip()
                else:
                    # Fall back to removing the prompt manually
                    summary = generated_text.replace(prompt, "").strip()
            
            # If the summary doesn't start with "I am", add it
            if not summary.startswith("I am"):
                if summary.startswith("a skilled"):
                    summary = "I am " + summary
                elif not any(summary.lower().startswith(starter) for starter in ["i ", "i'm", "i've", "i have"]):
                    summary = f"I am a skilled {job_title} with " + summary
            
            # Clean up common issues in GPT-2 generated text
            summary = re.sub(r'\s+', ' ', summary)  # Remove extra whitespace
            summary = re.sub(r'\.{2,}', '.', summary)  # Replace multiple periods with one
            
            # Ensure it ends with proper punctuation
            if not summary.endswith(('.', '!', '?')):
                summary += '.'
                
            # Limit to roughly 50-60 words
            words = summary.split()
            if len(words) > 60:
                summary = ' '.join(words[:60]) + '...'
                
            logger.info(f"Generated summary: {summary}")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            # Fallback for error cases
            return f"I am an experienced {job_title} with a proven track record of success and a passion for delivering results. My expertise lies in problem-solving, collaboration, and driving business growth through innovative solutions."
    
    def generate_skills(self, job_title):
        """Generate relevant skills for a given job title"""
        # Create a structured prompt with clear markers
        prompt = f"""
TASK: List important skills for a job position.
JOB TITLE: {job_title}
INSTRUCTIONS: List 10 technical and soft skills relevant to this position. Separate each skill with a comma.
SKILLS:
1."""
        
        try:
            # Generate text
            result = self.generator(
                prompt,
                max_length=200,
                min_length=50,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1
            )
            
            # Extract generated text
            generated_text = result[0]["generated_text"]
            
            # Extract just the skills part
            skills_pattern = r"SKILLS:\s*(.*?)(?:\n\n|$)"
            skills_match = re.search(skills_pattern, generated_text, re.DOTALL)
            
            if skills_match:
                skills_text = skills_match.group(1).strip()
            else:
                # Extract anything after "SKILLS:"
                parts = generated_text.split("SKILLS:")
                if len(parts) > 1:
                    skills_text = parts[1].strip()
                else:
                    skills_text = generated_text.replace(prompt, "").strip()
            
            # Process the skills text
            skills = self._process_skills_text(skills_text)
            
            logger.info(f"Generated skills: {skills}")
            return skills
            
        except Exception as e:
            logger.error(f"Error generating skills: {str(e)}")
            # Fallback for error cases based on job title
            return self._get_fallback_skills(job_title)
    
    def _process_skills_text(self, skills_text):
        """Extract and clean skills from generated text"""
        # Try to extract numbered skills first
        numbered_skills = re.findall(r'\d+\.\s*(.*?)(?=\d+\.|$)', skills_text, re.DOTALL)
        if numbered_skills:
            skills = [skill.strip() for skill in numbered_skills if skill.strip()]
        else:
            # If no numbered items, try splitting by commas
            if "," in skills_text:
                skills = [skill.strip() for skill in skills_text.split(",")]
            # If no commas, try newlines
            elif "\n" in skills_text:
                skills = [skill.strip() for skill in skills_text.split("\n")]
                # Check for bullet points
                skills = [s.lstrip('•- ') for s in skills]
            else:
                # If no structure, just use the whole text
                skills = [skills_text.strip()]
        
        # Clean up skills
        clean_skills = []
        for skill in skills:
            # Remove any numbering or bullets
            skill = re.sub(r'^\d+\.\s*', '', skill)
            skill = re.sub(r'^[•\-]\s*', '', skill)
            
            # Remove any trailing punctuation
            skill = skill.rstrip('.,;:')
            
            # Skip empty skills or ones that are too short
            if skill and len(skill) > 2:
                clean_skills.append(skill)
        
        # Remove duplicates while preserving order
        unique_skills = []
        seen = set()
        for skill in clean_skills:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        # Return at most 10 skills
        return unique_skills[:10]
    
    def _get_fallback_skills(self, job_title):
        """Provide fallback skills based on job title"""
        job_lower = job_title.lower()
        
        if any(term in job_lower for term in ["software", "developer", "engineer", "programming", "coder"]):
            return ["Problem Solving", "JavaScript", "Python", "SQL", "Git", 
                   "Communication", "Agile Methodologies", "APIs", "Testing", "Data Structures"]
                   
        elif any(term in job_lower for term in ["design", "designer", "ui", "ux", "graphic"]):
            return ["Adobe Creative Suite", "UI/UX Design", "Typography", "Wireframing", 
                   "Visual Communication", "Color Theory", "Figma", "User Research", 
                   "Prototyping", "Branding"]
                   
        elif any(term in job_lower for term in ["data", "analyst", "scientist", "analytics"]):
            return ["SQL", "Python", "Data Visualization", "Statistical Analysis", 
                   "Excel", "Machine Learning", "R", "Data Cleaning", 
                   "Critical Thinking", "Problem Solving"]
                   
        elif any(term in job_lower for term in ["manager", "management", "director", "lead"]):
            return ["Leadership", "Strategic Planning", "Team Management", "Communication", 
                   "Problem Solving", "Decision Making", "Time Management", 
                   "Project Management", "Negotiation", "Delegation"]
                   
        else:
            # Generic professional skills
            return ["Communication", "Problem Solving", "Team Collaboration", 
                   f"{job_title} expertise", "Time Management", "Project Management", 
                   "Analytical Thinking", "Adaptability", "Interpersonal Skills", "Leadership"]

# Initialize the generator instance
ai_generator = AIGenerator()