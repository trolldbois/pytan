$(function() {
    var scntDiv = $('#input_container');
    var i = $('#input_container p').size() + 1;


    $('#add').on('click', function() {
        $('<p><label for="input_box"><input type="text" size="80" name="computer_names" value="" placeholder="-- Computer Name --" /></label> <a href="#" id="remove">Remove</a></p>').appendTo(scntDiv);
        i++;
        // validate();
        return false;
    });

    $('#input_container').on('click', 'a#remove', function() {
        if( i > 2 ) {
            $(this).parents('p').remove();
            i--;
        }
        return false;
    });

    $("form").validate({
        rules: {
            computer_names: "required"
        },
        messages: {
            computer_names: "Please provide input for at least one computer name."
        }
    });

});
