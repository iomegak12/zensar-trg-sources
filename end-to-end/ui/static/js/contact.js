// Contact form functionality
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));

    // Form validation
    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();
        event.stopPropagation();

        // Remove existing validation states
        contactForm.classList.remove('was-validated');
        
        // Get form data
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData.entries());

        // Custom validation
        let isValid = true;
        const errors = {};

        // Validate required fields
        const requiredFields = ['firstName', 'lastName', 'email', 'subject', 'message'];
        requiredFields.forEach(field => {
            const element = document.getElementById(field);
            const value = data[field]?.trim();
            
            if (!value) {
                isValid = false;
                errors[field] = 'This field is required.';
                element.classList.add('is-invalid');
            } else {
                element.classList.remove('is-invalid');
                element.classList.add('is-valid');
            }
        });

        // Email validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (data.email && !emailPattern.test(data.email)) {
            isValid = false;
            errors.email = 'Please enter a valid email address.';
            document.getElementById('email').classList.add('is-invalid');
        }

        // Phone validation (optional but must be valid if provided)
        if (data.phone && data.phone.trim()) {
            const phonePattern = /^[\+]?[1-9][\d]{0,15}$/;
            const cleanPhone = data.phone.replace(/[\s\-\(\)]/g, '');
            if (!phonePattern.test(cleanPhone)) {
                isValid = false;
                errors.phone = 'Please enter a valid phone number.';
                document.getElementById('phone').classList.add('is-invalid');
            }
        }

        // Privacy policy agreement
        if (!document.getElementById('privacy').checked) {
            isValid = false;
            errors.privacy = 'You must agree to the privacy policy.';
            document.getElementById('privacy').classList.add('is-invalid');
        }

        if (!isValid) {
            contactForm.classList.add('was-validated');
            return;
        }

        // Show loading state
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status"></span>
            Sending...
        `;
        submitBtn.disabled = true;

        // Simulate form submission (replace with actual API call)
        setTimeout(() => {
            // Reset button state
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;

            // Save to localStorage for demonstration
            saveContactSubmission(data);

            // Reset form
            contactForm.reset();
            contactForm.classList.remove('was-validated');
            
            // Remove validation classes
            document.querySelectorAll('.is-valid, .is-invalid').forEach(el => {
                el.classList.remove('is-valid', 'is-invalid');
            });

            // Show success modal
            successModal.show();
        }, 2000);
    });

    // Real-time character count for message field
    const messageField = document.getElementById('message');
    const charCountDisplay = document.createElement('small');
    charCountDisplay.className = 'text-muted float-end mt-1';
    messageField.parentNode.appendChild(charCountDisplay);

    function updateCharCount() {
        const currentLength = messageField.value.length;
        const maxLength = 1000;
        charCountDisplay.textContent = `${currentLength}/${maxLength} characters`;
        
        if (currentLength > maxLength * 0.9) {
            charCountDisplay.className = 'text-warning float-end mt-1';
        } else {
            charCountDisplay.className = 'text-muted float-end mt-1';
        }
    }

    messageField.addEventListener('input', updateCharCount);
    updateCharCount(); // Initial count

    // Subject-based placeholder text for message field
    const subjectField = document.getElementById('subject');
    const placeholders = {
        'general': 'Tell us about your general inquiry...',
        'technical': 'Describe the technical issue you\'re experiencing...',
        'enterprise': 'Tell us about your enterprise requirements...',
        'partnership': 'Describe your partnership proposal...',
        'feedback': 'Share your feedback or suggestions...',
        'other': 'Please describe your inquiry...'
    };

    subjectField.addEventListener('change', function() {
        const selectedValue = this.value;
        if (placeholders[selectedValue]) {
            messageField.placeholder = placeholders[selectedValue];
        } else {
            messageField.placeholder = 'Tell us more about your inquiry...';
        }
    });

    // Auto-resize message textarea
    messageField.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
});

// Save contact submission to localStorage
function saveContactSubmission(data) {
    try {
        const submissions = JSON.parse(localStorage.getItem('contactSubmissions') || '[]');
        const submission = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            ...data
        };
        submissions.unshift(submission);
        
        // Keep only last 50 submissions
        if (submissions.length > 50) {
            submissions.splice(50);
        }
        
        localStorage.setItem('contactSubmissions', JSON.stringify(submissions));
        console.log('Contact submission saved:', submission);
    } catch (error) {
        console.error('Failed to save contact submission:', error);
    }
}

// Format time helper
function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
        return 'Today';
    } else if (diffDays === 2) {
        return 'Yesterday';
    } else if (diffDays <= 7) {
        return `${diffDays - 1} days ago`;
    } else {
        return date.toLocaleDateString();
    }
}