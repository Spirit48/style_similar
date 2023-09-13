$(function(){


  var docH = $(document).height();
  $('#wrap').height(docH)
    $('.sitemap').css('top', $('#wrap').height()-($('.sitemap').height()+180));

  


		// sub
		$('#snb li').not('.on').each(function(){
			var src = $(this).find('img').attr('src');
			$(this).hover(function(){
				$(this).find('img').attr('src', src.replace('off', 'on'));

			},function(){
				$(this).find('img').attr('src', src.replace('on', 'off'));
			});
		});




	});


	$(window).resize(function(){
		var docH = $(document).height();
		$('#wrap').height(docH)
			$('.sitemap').css('top', $('#wrap').height()-($('.sitemap').height()+180));
	});

