$(function(){
    tabEvt();

    $(document).on("click", ".fileAdd", function(){
        $(this).parents('.fileinputForm').find('.fileInput').click();
    });
    $(document).on("change", ".fileInput", function(){
        var v = $(this).val();
        $(this).parents('.fileinputForm').find('.fileTxt').val(v);
    });
});

function tabEvt(){
    let tabs = [];
        $('[data-tab-id]').on('click', function(){
            var tabid = $(this).data('tab-id');
            tabs.push(tabid);

            $(this).parent('li').addClass('on');
        tabs = [];
            $(this).parent('li').siblings().find('[data-tab-id]').each(function(){
            $(this).parent('li').removeClass('on');
            tabs.push($(this).data('tab-id'));
        });

            tabs.forEach(function(v){
            $('#'+v).hide();
        });
        $('#'+tabid).show();
    })
}


//팝업
function popClose(popup){
    let $popup = $(popup);
    $popup.fadeOut()
    $('body, html').css('overflow', '');
}

function popOpen(popup){
    let $popup = $(popup);
    $popup.fadeIn()
    $('body, html').css('overflow', 'hidden');
}
