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
		 $('.language-menu ul').removeClass('on')
		 })
 
 }
 

function fileAdd(){
	let $wrap;
	$('.inpFileadd .btn').on('click', function(){
		$wrap = $(this).parents('.inpFileadd');
		$wrap.find('input[type=file]').click();
	});	
	$('.inpFileadd input[type=file]').on('change', function(){
		let v = $(this).val();
		$wrap.find('input[type=text]').val(v);
	});

}


function footerInfo(){
	$('.js-footer .company-info .btn').on('click', function(){
			$('.js-footer .company-info').toggleClass('on');
			$('.js-footer .info').slideToggle();
	});

}



$(function(){
	gnbMenu();
	gnbMenuMobile();
	language();
	fileAdd();
	footerInfo();

});
