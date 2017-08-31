$(document).ready(function(){
var login = $("#login");
var register = $('#register');
var denglu = $('#denglu');
var zhuche = $('#zhuche');
login.css('display','block');
register.css('display','none');
denglu.click(function(){
   zhuche.removeClass('active');
   denglu.addClass('active');
   register.css('z-index','1');
   login.css('z-index','2');
	register.hide();
	login.show();
});
zhuche.click(function(){
   denglu.removeClass('active');
   zhuche.addClass('active');
   register.css('z-index','2');
   login.css('z-index','1');
	register.show();
	login.hide();
});

  $("#video1").click(function(){

    $.ajax({url:"static/json/json1.json",success:function(result){
        $("#json1").html(result.title);
        $("#json2").html(result.content);
    }});
  
    var myPlayer =  videojs("my-video");  //初始化视频-
    myPlayer.src("/static/video/video1.mp4");  //重置video的src
  
});

    $("#video2").click(function(){

    $.ajax({url:"static/json/jsoni2.json",success:function(result){
        $("#json1").html(result.title);
        $("#json2").html(result.content);
    }});

   
    var myPlayer =  videojs("my-video");  //初始化视频
    myPlayer.src("/static/video/video2.mp4");  //重置video的src
    
});
    $("#video3").click(function(){

    $.ajax({url:"static/json/json3.json",success:function(result){
        $("#json1").html(result.title);
        $("#json2").html(result.content);
    }});
    var myPlayer =  videojs("my-video");  //初始化视频
    myPlayer.src("/static/video/video3.mp4");  //重置video的src
  });

    $("#video4").click(function(){

    $.ajax({url:"static/json/json4.json",success:function(result){
        $("#json1").html(result.title);
        $("#json2").html(result.content);
    }});
    var myPlayer =  videojs("my-video");  //初始化视频
    myPlayer.src("/static/video/video4.mp4");  //重置video的src
  });

    $("#video5").click(function(){

    $.ajax({url:"static/json/json5.json",success:function(result){
        $("#json1").html(result.title);
        $("#json2").html(result.content);
    }});

    var myPlayer =  videojs("my-video");  //初始化视频
    myPlayer.src("/static/video/video5.mp4");  //重置video的src
  });
});
