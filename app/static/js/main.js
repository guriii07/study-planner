document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('studyForm');
    const addTopicBtn = document.getElementById('addTopicBtn');
    const syllabusContainer = document.getElementById('syllabusContainer');
    const loadingState = document.getElementById('loadingState');
    const scheduleOutput = document.getElementById('scheduleOutput');

    // 1. Feature to let students add as many topics as they need
    addTopicBtn.addEventListener('click', () => {
        const row = document.createElement('div');
        row.className = 'flex gap-2 mb-2 topic-row';
        row.innerHTML = `
            <input type="text" placeholder="Topic Name" class="topic-name flex-1 p-2 rounded-lg border-none shadow-sm outline-none">
            <select class="topic-confidence p-2 rounded-lg border-none shadow-sm outline-none bg-white">
                <option value="weak">Weak 😥</option>
                <option value="medium">Medium 😐</option>
                <option value="strong">Strong 😎</option>
            </select>
            <button type="button" class="remove-btn text-red-400 font-bold px-2 hover:text-red-600">✕</button>
        `;
        
        // Add delete functionality to the new 'X' button
        row.querySelector('.remove-btn').addEventListener('click', () => row.remove());
        
        // Insert it right above the "Add topic" button
        syllabusContainer.insertBefore(row, addTopicBtn);
    });

    // 2. Handle the Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Stop page refresh
        
        // Clear old results and show loading animation
        scheduleOutput.innerHTML = '';
        loadingState.classList.remove('hidden');
        
        // Gather the syllabus data from all the input rows
        const syllabus = [];
        document.querySelectorAll('.topic-row').forEach(row => {
            const topicName = row.querySelector('.topic-name').value.trim();
            const confidence = row.querySelector('.topic-confidence').value;
            if (topicName) {
                syllabus.push({ topic: topicName, confidence: confidence });
            }
        });

        // Package the data exactly how our Flask backend expects it
        const studentData = {
            exam_name: document.getElementById('examName').value,
            exam_date: document.getElementById('examDate').value,
            daily_hours: parseFloat(document.getElementById('dailyHours').value),
            syllabus: syllabus
        };

        try {
            // Send the POST request to the Flask API
            const response = await fetch('/api/generate-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData)
            });

            const result = await response.json();

            if (!response.ok) throw new Error(result.error || 'Something went wrong');

            // Render the aesthetic UI cards with the returned JSON
            renderSchedule(result.data.schedule);
            
        } catch (error) {
            scheduleOutput.innerHTML = `<div class="p-4 bg-red-100 text-red-700 rounded-xl text-center font-semibold">Error: ${error.message}</div>`;
        } finally {
            // Hide the loading text once finished
            loadingState.classList.add('hidden');
        }
    });

    // 3. The Function to Build the Cozy Cards
    function renderSchedule(dailyPlans) {
        dailyPlans.forEach(dayPlan => {
            // Format the topics nicely with emojis
            const topicsHtml = dayPlan.topics.map(t => `<li class="flex items-center gap-2">✨ <span>${t}</span></li>`).join('');
            
            // Build the card using Tailwind classes for that glass/pastel vibe
            const card = document.createElement('div');
            card.className = 'glass-card p-6 border-l-8 border-matcha transition transform hover:-translate-y-1 hover:shadow-lg';
            
            card.innerHTML = `
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <span class="text-sm font-bold text-gray-400 uppercase tracking-wider">Day ${dayPlan.day} • ${dayPlan.date}</span>
                        <h3 class="text-xl font-bold text-textDark mt-1">Focus: ${dayPlan.estimated_hours} Hours</h3>
                    </div>
                </div>
                
                <div class="bg-white bg-opacity-60 p-4 rounded-xl mb-4">
                    <p class="italic text-gray-700 font-medium">"${dayPlan.vibe_message}"</p>
                </div>
                
                <div class="mb-4">
                    <h4 class="font-bold text-gray-600 mb-2">Topics to Cover:</h4>
                    <ul class="space-y-1 text-gray-800">
                        ${topicsHtml}
                    </ul>
                </div>
                
                <div class="bg-peach bg-opacity-30 p-4 rounded-xl text-sm text-gray-700">
                    <strong class="block mb-1">🌿 Mindful Break Idea:</strong>
                    ${dayPlan.break_suggestion}
                </div>
            `;
            
            scheduleOutput.appendChild(card);
        });
    }
});