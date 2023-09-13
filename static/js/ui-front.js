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
        let $siblings = $(this).parents('.list').find('li').not($(this).parent());

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
    $('.js-footer .client .btn').on('click', function(){
        $('.js-footer .client').toggleClass('on');
        $('.js-footer .info').slideToggle();
    });
}

function noticeTab(){
    $('.js-tab-board-tit a').on('click', function(){
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
    let list = [];
    $('.js-gallery-slide').each(function(i){
        $(this).addClass('js-gallery-slide-order'+i);
        list.push('js-gallery-slide-order'+i);
    });

    for(let i= 0; i<=list.length;i++){
        let num = $('.'+list[i]).data('slide');
        let group = $('.'+list[i]).data('group');
        let auto =  $('.'+list[i]).data('auto') === 'auto' ? true : false;

        var swiper = new Swiper('.'+list[i], {
            loop: auto,
            autoplay: auto,
            slidesPerView: 1,
            slidesPerGroup : group ? group : 1,
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
}

function gallery2(){
    var swiper = new Swiper(".js-gallery-slide-two", {
        slidesPerView: 1,
        spaceBetween: 15,
        slidesPerView: "auto",
    });
}

function mainKeySlide(){
    if($('.js-main-key-slider').length <=0) return;
    let list = [];
    $('.js-main-key-slider').each(function(i){
        if($(this).find('.swiper-slide').length <= 1) return;
        $(this).addClass('js-main-key-slider'+i);
        list.push('js-main-key-slider'+i);
    });

    for(let i= 0; i<list.length;i++){
        var swiper = new Swiper('.'+list[i], {
            loop: true,
            autoplay:true,
            slidesPerView: 1,
            // spaceBetween: 15,
            pagination: {
                el: '.'+list[i] +" .swiper-pagination",
                clickable: true,
            },
        });
    }
}

function listWrapSlide(slide){
    let list = [];
    $(slide).each(function(i){
        $(this).addClass(slide.split('.')[1]+i);
        list.push(slide.split('.')[1]+i);
    });

    if(list.length <= 0) return;
    setTimeout(function(){
        for(let i= 0; i<=list.length;i++){
            let num = $('.'+list[i]).data('tablet') ? $('.'+list[i]).data('tablet') : 1
            var swiper = new Swiper('.'+list[i], {
                loop: true,
                autoplay:true,
                slidesPerView: 1,
                spaceBetween: 15,
                pagination: {
                    el: '.js-list-wrap-slide'+i +" .swiper-pagination",
                    clickable: true,
                },
                breakpoints: {
                    480: {
                        slidesPerView: 1,
                    },
                    481: {
                        slidesPerView: num,
                    },
                    1024: {
                        slidesPerView: 1,
                    },
                },
            });
        }
    }, 300);
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
        let $this = $(this);
        setTimeout(function(){
            let w = $this.find('[data-tab-id]').eq(0).outerWidth();
            if($this.find('.indicator').length <=0 ){
                $this.append('<span class="indicator" style="left:0;width:'+w+'px" ></span>');
            }else{
                $this.find('.indicator').width(w);
            }
        }, 300)
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
            layer.addClass('on');
            $('.js-language .selected').addClass('on');
        }else{
            layer.removeClass('on');
            $('.js-language .selected').removeClass('on');
        }

        $(document).on('click', '.js-language ul li a', function(){
            var txt = $(this).parent().attr('class')
            selected.text(txt);

            layer.removeClass('on');
            $('.js-language .selected').removeClass('on');
        });
    });

    $(window).on('resize', function(){
    $('.js-language .selected').removeClass('on')
    $('.js-language ul').removeClass('on')
    })
}

function galleryclose(){
    $('.gallery-show-wrap').addClass('hidden-ani');
    setTimeout(() => {
      $('.gallery-show-wrap').removeClass('hidden-ani');
      $('.gallery-show-wrap').addClass('hidden');
    }, 500);
}

function galleryOpen(){
    $('.gallery-list-item a').on('click', function(){
        let num = $(this).parents('.gallery-list-item').index();
        fn(num)

        function fn(num){
            if($('.js-gallery-show .swiper-wrapper .swiper-slide').length <= 0){
                $('.js-gallery-show-list .gallery-list-item').each(function(){
                let src = $(this).find('img').attr('src');
                let txt = $(this).find('.txt').text();
                let item ='<li class="swiper-slide">'+
                        '<div class="img">'+
                            '<img src="'+src+'" alt="">'+
                        '</div>'+
                        '<div class="desc">'+
                            '<div class="txt">'+
                                txt+
                            '</div>'+
                        '</div>'+
                    '</li>';

                    $('.js-gallery-show .swiper-wrapper').append(item);
                });
            }

            $('.gallery-show-wrap').removeClass('hidden');
            $('.gallery-show-list .img img').each(function(i){
                let len = $('.gallery-grid .item').length;
                let src = $(this).attr('src');
                $(this).parents('.img').css('background-image', 'url('+src+')')
            });

            gallerySwiper = undefined;

            function initSwiper(){
                var screenWidth = $(window).width();

                gallerySwiper = new Swiper('.swiper-container',{
                    grabCursor: true,
                    centeredSlides: true,
                    slidesPerView: "auto",
                    centeredSlides: true,
                    pagination: {
                        el: ".swiper-pagination",
                        type: "fraction",
                    },
                    navigation: {
                        nextEl: ".swiper-button-next",
                        prevEl: ".swiper-button-prev",
                    },
                });
                gallerySwiper.slideTo(num, 0);
            }

            initSwiper();
            let resizeCheck;
            $(window).on('resize', function(){
                resizeCheck = setTimeout(function(){
                    gallerySwiper.update()
                },500);
            });
        }
    });
}

$(function(){
    gnbMenu();
    gnbMenuMobile();
    footerInfo();
    noticeTab();
    gallery();
    gallery2();
    mainKeySlide();
    listWrapSlide('.js-list-wrap-slide');
    listWrapSlide('.js-list-wrap-slide-type2');
    shortcutMenu();
    faqList();
    tabEvt();
    language();
    galleryOpen();
});

$(window).on('resize', function(){
    tabEvt();
})