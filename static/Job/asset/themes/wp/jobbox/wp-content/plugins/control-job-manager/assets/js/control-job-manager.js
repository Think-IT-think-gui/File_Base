jQuery(document).ready(function($){
    'use strict';

    // Filter
    $('.dropdown-sort').off('click').on('click', 'a', function(){
        $(this).closest('.dropdown-sort').find('input').attr('value', $(this).data('value')).trigger('change');
    });

    // skills
    $( "#new-tag-ctrljm_skill" ).autocomplete({
        source: controlJobManager.skills
    });

    // Apply now
    $(document).on('click', '.ctrljm-apply-now', function(){
        var data = {
            'action': 'ctrljm_apply_action',
            'job_id': $(this).data('id')
        };
        // We can also pass the url value separately from ajaxurl for front end AJAX implementations
        $.post(controlJobManager.ajax, data, function(response) {           
            $('#ModalApplyJobForm #post_title').val(  response.title);
            if(response.hasOwnProperty('full_name')){
                $('#ModalApplyJobForm #applicants_full_name').val(  response.full_name);
            }
            if(response.hasOwnProperty('email')){
                $('#ModalApplyJobForm #applicants_email').val(  response.email);
            }
            if(response.hasOwnProperty('job_id')){
                $('#ModalApplyJobForm #job_id').val(  response.job_id);
            }
        });
    });
})