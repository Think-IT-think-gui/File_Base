jQuery(document).ready(function($) {
    if($(".input-keysearch").length > 0){
        $(".input-keysearch").autocomplete({
            source: JOBBOX.keywords,
            minLength: 2 // Adjust the minimum characters required before autocomplete starts
        });
    }
});