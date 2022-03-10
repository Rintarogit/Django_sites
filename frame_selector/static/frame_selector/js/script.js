// ヘッダーレスポンシブ対応
const responsive_menu_btn = document.querySelector('.responsive_btn');
responsive_menu_btn.addEventListener('click', menuToggle);
function menuToggle() {
  const header_menu_detail = document.querySelector('.header_nav');
  header_menu_detail.classList.toggle('menu_active');
  $(".container").toggle();  // メニュー表示中は中身を閉じる
}
// 画面スクロールに合わせてヘッダーを透過させる。
$(document).ready(function() {
  $(window).scroll(function() {
    if ($(this).scrollTop() > 0) {
      $('header').css('opacity', 0.8);
    } else {
      $('header').css('opacity', 1);
    }
  });
});

// 背景画像（パララックス設定）
$(function() {
  $(window).scroll(function(){
      var scroll = $(this).scrollTop(); // スクロール値を取得
      $('body').css('background-position', '0' + parseInt( -scroll / 4 ) + 'px'); // 1/4のスピード
    }); 
});


// 列スイッチの表示切替ボタン
$(function() {
	$('.selectBtn a').click(function() {
		if($(this).html() == 'OPEN'){
			$(this).html('CLOSE');
		}else{
			$(this).html('OPEN');
		}
		$('.selectItem').slideToggle();
		return false;
	});
});





// 動きのきっかけの起点となるアニメーションの名前を定義
function BgFadeAnime(){

    // 背景色が伸びて出現（左から右）
  $('.bgLRextendTrigger').each(function(){ //bgLRextendTriggerというクラス名が
    var scroll = $(window).scrollTop();
    var windowHeight = $(window).height();
    var elemPos = windowHeight*0.6;

    if (scroll >= windowHeight - elemPos){
      $(this).addClass('bgLRextend');// 画面内に入ったらbgLRextendというクラス名を追記
    }else{
      $(this).removeClass('bgLRextend');// 画面外に出たらbgLRextendというクラス名を外す
    }
  }); 

  // 文字列を囲う子要素
  $('.bgappearTrigger').each(function(){ //bgappearTriggerというクラス名が
    var scroll = $(window).scrollTop();
    var windowHeight = $(window).height();
    var elemPos = windowHeight*0.6;

    if (scroll >= windowHeight - elemPos){
        $(this).addClass('bgappear');// 画面内に入ったらbgappearというクラス名を追記
    }else{
      $(this).removeClass('bgappear');// 画面外に出たらbgappearというクラス名を外す
    }
  }); 
  
  $('#inner_area p').delay(1000).fadeOut(5000);
}

// 画面をスクロールをしたら動かす
$(window).scroll(function (){
  BgFadeAnime();/* アニメーション用の関数を呼ぶ*/

});