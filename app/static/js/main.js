// Main JavaScript for Resume Screener Application

// Document ready function
$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Enable file input filename display
    $('.custom-file-input').on('change', function() {
        var fileName = $(this).val().split('\\').pop();
        $(this).next('.custom-file-label').addClass('selected').html(fileName);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 5000);
    
    // Initialize password strength meter
    if ($('#password').length) {
        $('#password').on('input', function() {
            var password = $(this).val();
            var strength = 0;
            
            // Check password strength
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]+/)) strength++;
            if (password.match(/[A-Z]+/)) strength++;
            if (password.match(/[0-9]+/)) strength++;
            if (password.match(/[!@#$%^&*(),.?":{}|<>]+/)) strength++;
            
            // Update strength indicator
            var strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
            var strengthClass = ['danger', 'warning', 'info', 'primary', 'success', 'success'];
            
            $('#password-strength').text(strengthText[strength] || '');
            $('#password-strength').removeClass().addClass('text-' + (strengthClass[strength] || 'muted'));
            
            // Update progress bar
            var width = (strength / 5) * 100;
            $('#password-strength-bar').css('width', width + '%').removeClass().addClass('progress-bar bg-' + (strengthClass[strength] || 'muted'));
        });
    }
    
    // Confirm password match
    if ($('#password2').length) {
        $('#password2').on('input', function() {
            var password = $('#password').val();
            var confirmPassword = $(this).val();
            
            if (confirmPassword !== '') {
                if (password === confirmPassword) {
                    $(this).removeClass('is-invalid').addClass('is-valid');
                    $('#password-match').text('Passwords match!').removeClass('text-danger').addClass('text-success');
                } else {
                    $(this).removeClass('is-valid').addClass('is-invalid');
                    $('#password-match').text('Passwords do not match').removeClass('text-success').addClass('text-danger');
                }
            } else {
                $(this).removeClass('is-valid is-invalid');
                $('#password-match').text('');
            }
        });
    }
    
    // Handle resume upload form submission
    $('#resume-upload-form').on('submit', function(e) {
        var fileInput = $('#resume')[0];
        var file = fileInput.files[0];
        var maxSize = 16 * 1024 * 1024; // 16MB
        
        if (file && file.size > maxSize) {
            e.preventDefault();
            alert('File size exceeds the 16MB limit. Please choose a smaller file.');
            return false;
        }
        
        // Show loading state
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.html();
        submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading...');
        
        return true;
    });
    
    // Initialize DataTables if present
    if ($.fn.DataTable) {
        $('.datatable').DataTable({
            responsive: true,
            pageLength: 10,
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, 'All']],
            language: {
                search: "_INPUT_",
                searchPlaceholder: "Search...",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                infoEmpty: "Showing 0 to 0 of 0 entries",
                infoFiltered: "(filtered from _MAX_ total entries)",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            },
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                 "<'row'<'col-sm-12'tr>>" +
                 "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>"
        });
    }
    
    // Handle delete confirmation
    $('.confirm-delete').on('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        var message = $(this).data('confirm') || 'Are you sure you want to delete this item?';
        
        if (confirm(message)) {
            window.location.href = url;
        }
    });
    
    // Initialize chart if present
    if (typeof Chart !== 'undefined' && $('#resumeChart').length) {
        var ctx = document.getElementById('resumeChart').getContext('2d');
        var chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Skills Match', 'Experience Match', 'Education Match', 'Missing'],
                datasets: [{
                    data: [65, 20, 10, 5],
                    backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#e74a3b'],
                    hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#be2617'],
                    hoverBorderColor: 'rgba(234, 236, 244, 1)',
                }],
            },
            options: {
                maintainAspectRatio: false,
                tooltips: {
                    backgroundColor: 'rgb(255,255,255)',
                    bodyFontColor: '#858796',
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    caretPadding: 10,
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                    }
                },
                cutoutPercentage: 70,
            },
        });
    }
    
    // Handle tab persistence
    $('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('lastTab', $(e.target).attr('href'));
    });
    
    var lastTab = localStorage.getItem('lastTab');
    if (lastTab) {
        $('[href="' + lastTab + '"]').tab('show');
    }
    
    // Initialize select2 if present
    if ($.fn.select2) {
        $('.select2').select2({
            theme: 'bootstrap4',
            width: '100%',
            placeholder: 'Select an option',
            allowClear: true
        });
    }
    
    // Add animation to elements with animate-on-scroll class
    function animateOnScroll() {
        $('.animate-on-scroll').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            
            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).addClass('fade-in');
            }
        });
    }
    
    // Run on page load and scroll
    animateOnScroll();
    $(window).on('scroll', animateOnScroll);
});

// Utility function to show loading state on buttons
function setButtonLoading(button, isLoading) {
    var $button = $(button);
    var originalText = $button.html();
    
    if (isLoading) {
        $button.data('original-text', originalText);
        $button.prop('disabled', true);
        $button.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...');
    } else {
        $button.prop('disabled', false);
        $button.html($button.data('original-text') || originalText);
    }
}

// Utility function to show toast notifications
function showToast(title, message, type = 'info') {
    var toastId = 'toast-' + Math.random().toString(36).substr(2, 9);
    var toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <strong>${title}</strong><br>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    $('#toast-container').append(toastHtml);
    var toastElement = document.getElementById(toastId);
    var toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 5000 });
    toast.show();
    
    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function () {
        $(this).remove();
    });
}

// Handle AJAX form submissions
$(document).on('submit', '.ajax-form', function(e) {
    e.preventDefault();
    
    var $form = $(this);
    var $submitBtn = $form.find('button[type="submit"]');
    var formData = new FormData(this);
    var method = $form.attr('method') || 'POST';
    var action = $form.attr('action') || window.location.href;
    var dataType = $form.data('type') || 'json';
    
    // Show loading state
    setButtonLoading($submitBtn, true);
    
    $.ajax({
        url: action,
        type: method,
        data: formData,
        processData: false,
        contentType: false,
        dataType: dataType,
        success: function(response) {
            if (response.redirect) {
                window.location.href = response.redirect;
            } else if (response.message) {
                showToast(response.title || 'Success', response.message, response.type || 'success');
                
                if (response.reload) {
                    setTimeout(function() {
                        window.location.reload();
                    }, 1500);
                }
                
                if (typeof response.callback === 'function') {
                    response.callback(response);
                }
            }
            
            // Reset form if needed
            if (response.resetForm) {
                $form.trigger('reset');
            }
        },
        error: function(xhr) {
            var errorMessage = 'An error occurred. Please try again.';
            
            try {
                var response = JSON.parse(xhr.responseText);
                if (response.message) {
                    errorMessage = response.message;
                }
            } catch (e) {
                console.error('Error parsing error response:', e);
            }
            
            showToast('Error', errorMessage, 'danger');
        },
        complete: function() {
            setButtonLoading($submitBtn, false);
        }
    });
});

// Initialize tooltips on dynamically added elements
$(document).on('mouseover', '[data-bs-toggle="tooltip"]', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
