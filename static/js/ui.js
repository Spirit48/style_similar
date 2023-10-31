function gnbMenu(){
    // gnbMenu
    var toggling = false;
    var obj = $('.js-gnb-sub');
    
    function slidein(){
        $(obj).stop().slideDown(300);
        $('.gnb-sub-wrap .dim').fadeIn();
    }
    function slideout(){
        $(obj).stop().slideUp(200, function(){
            $(obj).attr('style', '');
            $('.gnb-sub-wrap .dim').fadeOut();
        });
    }
    function over(){
        //web - gnbOver
        $('.js-header').on('mouseover', function(e) {
            if($('.js-header .gnb-menu .list, .js-header .gnb-sub').has(e.target).length){
                clearTimeout(toggling);
                toggling = setTimeout(slidein, 300);
            }else{
                clearTimeout(toggling);
                setTimeout(slideout, 300);
            }
        });
        $('.js-header').on('mouseleave', function(e) {
            clearTimeout(toggling);
            setTimeout(slideout, 300);
        });        
    }    

    over()


    $(window).scroll(function(){
        $('.js-gnb-sub').hide()
    });
}

function gnbMenuMobile(){

    $('.js-gnb-menu .list li').each(function(){
        if($(this).find('ul').length > 0){
            $(this).addClass('has-menu');
            if($(this).hasClass('on')){
                $(this).addClass('menu-on')
                $(this).children('ul').show();
            }
        }
    });

    $(document).on('click', '.js-gnb-menu  .list li > a', function(){

        let $parent = $(this).parent();
        let $menu = $(this).next('ul');
        let $siblings = $(this).parent().siblings();

        $siblings.removeClass('on');
        if($parent.hasClass('on')){
            $parent.removeClass('on');
        }else{
            $parent.addClass('on');
        }
        $siblings.removeClass('menu-on');
        $siblings.find('ul').slideUp(220);
        $siblings.find('li').removeClass('on');
        $siblings.find('li').removeClass('menu-on');

        if($parent.hasClass('has-menu')){
            if($menu.is(':hidden')){
                $parent.addClass('menu-on');
                $menu.slideDown(220);
            }else{
                $parent.removeClass('menu-on');
                $menu.slideUp(220);
            }
        }
    })

    $('.mMenu').on('click', function () {
        var target = $('.gnb-menu');
        if (target.is(':hidden')) {
            $('body, html').css('overflow', 'hidden');
                target.addClass('on');
                target.find('.inner').animate({ right: 0 }, 300, function () {
                        target.find('.close').fadeIn();
                });
                target.find('.mask').fadeIn();
        } else {
            mMenuClose();
        }
});
$('.js-gnb-menu .mask').on('click', function () {
        mMenuClose();
});

function mMenuClose() {
    $('body, html').css('overflow', '');
        var target = $('.gnb-menu');
        target.find('.inner').stop().animate({ right: -300 }, 300, function () {
                target.removeClass('on');
        });
        target.find('li').removeClass('on menu-on');
        target.find('li ul').hide();
        target.find('.mask').fadeOut();
        target.find('.close').fadeOut();
    }

    $(window).on('resize', mMenuClose)
}


function footerInfo(){
    $('.js-footer .company-info .btn').on('click', function(){
        $('.js-footer .company-info').toggleClass('on');
        $('.js-footer .info').slideToggle();
    });

}

function noticeTab(){
    $('.js-tab-board-title a').on('click', function(){
        var href= $(this).attr('href');
        var siblings = $(this).siblings('a')
        siblings.each(function(){
                var h = $(this).attr('href');
                $(this).removeClass('on');
                $(h).hide();
        });
        $(this).addClass('on');
        $(href).show();

        return false;
});
}

function gallery(){
    let num = $('.js-gallery-slide').data('slide');
    var swiper = new Swiper(".js-gallery-slide", {
        slidesPerView: 1,
        spaceBetween: 15,
        // pagination: {
        //     el: ".swiper-pagination",
        //     clickable: true,
        // },
        breakpoints: {
            480: {
                slidesPerView: 2,
            },
            640: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 3,
            },
            1024: {
                slidesPerView: num,
            },
        },
    });
}

function gallery2(){
    var swiper = new Swiper(".js-gallery-slide-two", {
        slidesPerView: 1,
        spaceBetween: 15,
        slidesPerView: "auto",
    });
}

function listWrapSlide(){
    var swiper = new Swiper(".js-list-wrap-slide", {
        slidesPerView: 1,
        spaceBetween: 15,
        pagination: {
            el: ".js-list-wrap-slide .swiper-pagination",
            clickable: true,
        },
        breakpoints: {
            480: {
                slidesPerView: 1,
            },
            481: {
                slidesPerView: 2,
            },
            1025: {
                slidesPerView: 1,
            },
        },
    });
}

function shortcutMenu(){
    $('.js-shortcut-menu > ul > li > a').on('click', function(){
        if($(this).next('ul').is(':hidden')){
                $(this).addClass('on');
                $(this).next('ul').slideDown();
        }else{
    $(this).removeClass('on');
                $(this).next('ul').slideUp();
        }
})
}

function faqList(){
    if($('.js-faq-answer').length <= 0) return;
    // faqList2
    $('.js-faq-question').toggleClass('inactive-header');
    $('.js-faq-question').first().toggleClass('active-header').toggleClass('inactive-header');
    $('.js-faq-answer').first().slideDown().toggleClass('open-content');

    $('.js-faq-question').click(function () {
        if($(this).is('.inactive-header')) {
            $('.active-header').toggleClass('active-header').toggleClass('inactive-header').next().slideToggle().toggleClass('open-content');
            $(this).toggleClass('active-header').toggleClass('inactive-header');
            $(this).next().slideToggle().toggleClass('open-content');
        }

        else {
            $(this).toggleClass('active-header').toggleClass('inactive-header');
            $(this).next().slideToggle().toggleClass('open-content');
        }
    });
}
function tabEvt(){
    $('.js-tab-type-line').each(function(){
        let w = $(this).find('[data-tab-id]').eq(0).outerWidth();
        if($(this).find('.indicator').length <=0 ){
            $(this).append('<span class="indicator" style="left:0;width:'+w+'px" ></span>');
        }else{
            $(this).find('.indicator').width(w);
        }
    });

  let tabs = [];
    $('[data-tab-id]').on('click', function(){

        var tabid = $(this).data('tab-id');
        var pos = $(this).position().left;
        var w = $(this).outerWidth()
        var $siblings = $(this).parent('li').length > 0 ? $(this).parent('li').siblings().find('[data-tab-id]') : $(this).siblings('[data-tab-id]')

        tabs = [];
        tabs.push(tabid);

        $(this).append('<span class="effect-ripple effect-rippleVisible"><span class="effect-child effect-childLeaving"></span></span>')
        setTimeout(function(){
            $('.effect-ripple').remove();
        }, 300)
        $(this).parent().find('.indicator').css({ left: pos, width: w });

        $(this).addClass('on');
        $(this).parent('li').addClass('on');
        $siblings.each(function(){
          $(this).removeClass('on');
              $(this).parent('li').removeClass('on');
          tabs.push($(this).data('tab-id'));
        });

        tabs.forEach(function(v){

          $('#'+v).hide();
        });
        $('#'+tabid).show();

   });
}

function language(){

 $(document).on('click', '.js-language .selected', function(){

    var layer = $(this).next('ul');
    var selected = $('.js-language').find('.selected em');
    if(layer.is(':hidden')){
        layer.stop().slideDown(300);
        $('.js-language .selected').addClass('on');
    }else{
        layer.stop().slideUp(300);
        $('.js-language .selected').removeClass('on');
    }

   $(document).on('click', '.js-language ul li a', function(){
        var txt = $(this).text();
        selected.text(txt);

        layer.stop().slideUp(300);
        $('.js-language .selected').removeClass('on');
      });

  });

}

$(function(){
    gnbMenu();
    gnbMenuMobile();
    footerInfo();
    noticeTab();
    gallery();
    gallery2();
    listWrapSlide();
    shortcutMenu();

    faqList();
    tabEvt();

    language();
});

$(window).on('resize', function(){
    tabEvt();
})