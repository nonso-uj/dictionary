window.onload = function(){
    $('#myModal').modal('show');
    $('#word-form').hide();
    $('#logo-form').hide();
    $('.edit-word, .edit-meaning').hide();
    $('.submit, .cancel').parent().hide();

    // ALL WORDS BUTTON
    $('#uno').click(function(){
        location.reload();
    });


    // TOGGLING ADD WORD BUTTON
    $('#deux').click(function(){
        $('#uno, #logo-add').removeClass('side-active');
        $(this).addClass('side-active');
        $('#word-form').show();
        $('#logo-form').hide();
    });

    $('#cancel').click(function(){
        location.reload();
    });


    // CREATION OPERATION
    $('#word-form').submit(function(){
        let word = $('#word').val();
        let meaning = $('#meaning').val();

        $.ajax({
            url: '/word',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'word' : word,
                'meaning': meaning
            }),
            contentType: 'application/json, charset=UTF8',
            success: function(data){
                location.reload();
            },
            error: function(err){
                console.log(err)
            }
        });
    });


    // ADD LOGO OPERATION
    $('#logo-add').click(function(){
        $('#uno, #deux').removeClass('side-active');
        $(this).addClass('side-active');
        $('#logo-form').show();
        $('#word-form').hide();
    });

    $('#logo-cancel').click(function(){
        location.reload();
    });


    $('#logo-form').submit(function(){
        let data = new FormData();
        data.append('file', $('#logo')[0].files[0]);

        $.ajax({
            url: '/add_logo',
            type: 'POST',
            data: data,
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            success: function(data){
                location.reload();
            },
            error: function(err){
                console.log(err);
            }
        });
    });


    // DELETE OPERATION
    $('.delete').click(function(){
        let word_id = $(this).attr('id');

        $.ajax({
            url: '/word/' + word_id + '/delete',
            type: 'POST',
            success: function(data){
                location.reload();
            },
            error: function(err){
                console.log(err);
            }
        });
    });


    // UPDATE OPERATION
    $('.edit').click(function(){
        let parent = $(this).parents('tr');
        parent.find('.edit-word, .edit-meaning').show();
        parent.find('.word-word, .word-meaning').hide();
        parent.find('.submit, .cancel').parent().show();
        parent.find('.edit, .delete').parent().hide();
    });

    $('.cancel').click(function(){
        location.reload();
    });


    $('.update-form').submit(function(){
        let parent = $(this).parents('tr');
        let word = parent.find('input').val();
        let meaning = parent.find('textarea').val();
        let word_id = parent.find('.submit').attr('id');

        $.ajax({
            url:'/word/' + word_id + '/edit',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'word' : word,
                'meaning' : meaning
            }),
            contentType: 'application/json, charset=UTF-8',
            success: function(data){
                location.reload();
            },
            error: function(err){
                console.log(err);
            }
        });
    });






}

