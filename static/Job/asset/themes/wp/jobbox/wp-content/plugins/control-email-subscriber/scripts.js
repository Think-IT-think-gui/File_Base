jQuery(document).ready(function($) {
    "use strict";  

    function controlEmailSubscribercallbackMC(response){
        var responseSelector =  $('#mc-response');
        if (response.result === 'success') {
            responseSelector.empty().html('<p class="mb-0 alert alert-success text-success bg-light alert-dismissible">'+response.msg.replace('0 - ', '')+'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></p>');
        }else{
            responseSelector.empty().html('<p class="mb-0 alert alert-error text-danger bg-light alert-dismissible">'+response.msg.replace('0 - ', '')+'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></p>');
        }
    }
    $('#mc-form .btn').on('click', function(){
        if(controlEmailSubscriber.ajaxchimpurl != ''){
            $('#mc-form').ajaxChimp({
                url: controlEmailSubscriber.ajaxchimpurl,
                callback: controlEmailSubscribercallbackMC
            });
        }else{
            controlEmailSubscribercallbackMC({
                'result' : 'error',
                'msg' : 'Invalid mailchimp form settings'
            });
            return false;
        }
        
    });
    
    
    $( ".control-email-subscriber-form").submit(function() {
        var subscriptionForm = $(this);
        
       
        var form_data = new FormData();

        subscriptionForm.find('[type="submit"]').prop('disabled');
        form_data.append('action', 'control_email_subscriber_form_submit');
        form_data.append('form_values', subscriptionForm.serialize());      
       

        $.ajax({
            url: controlEmailSubscriber.ajaxurl,
            type: 'POST',
            contentType: false,
            processData: false,
            data: form_data,
            success: function (response) {      
                var message;          
                if (response.status == 0){
                    message = response.message;
                    subscriptionForm[0].reset();
                }else if (response.status == -1){
                    message = response.message;
                }else{
                    message = response;
                }  

                alert(message);
                subscriptionForm.find('[type="submit"]').prop('enabled');           
                
            }
        });

        return false;
    });
});