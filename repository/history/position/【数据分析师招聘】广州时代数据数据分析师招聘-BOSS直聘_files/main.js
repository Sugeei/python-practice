function loadCss(e){var t=document.createElement("link");t.type="text/css",t.rel="stylesheet",t.href=e,document.getElementsByTagName("head")[0].appendChild(t)}function seriesLoadScripts(e,t){if("object"!=typeof e)var e=[e];var o=document.getElementsByTagName("head").item(0)||document.documentElement,i=new Array,n=e.length-1,s=function(r){i[r]=document.createElement("script"),i[r].setAttribute("type","text/javascript"),i[r].onload=i[r].onreadystatechange=function(){this.onload=this.onreadystatechange=null,this.parentNode.removeChild(this),r!=n?s(r+1):"function"==typeof t&&t()},i[r].setAttribute("src",e[r]),o.appendChild(i[r])};s(0)}function isVisiable(e){if(e){var t=e.getBoundingClientRect();return t.top>0&&window.innerHeight-t.top>0||t.top<=0&&t.bottom>=0}}function isEmptyObject(e){var t;for(t in e)return!1;return!0}function getQueryString(e){var t=new RegExp("(^|&)"+e+"=([^&]*)(&|$)"),o=window.location.search.substr(1).match(t);return null!=o?unescape(o[2]):null}function localStorageInstance(e,t){if(window.localStorage)if(""===t)window.localStorage.removeItem(e);else{if(0!=t&&!t)return window.localStorage[e];window.localStorage[e]=t}else if(""===t)cookie.clearcookie(e);else{if(0!=t&&!t)return cookie.get(e);cookie.set(e,t,1e4)}}function getUuid(e,t){var o,i="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split(""),n=[];if(t=t||i.length,e)for(o=0;o<e;o++)n[o]=i[0|Math.random()*t];else{var s;for(n[8]=n[13]=n[18]=n[23]="-",n[14]="4",o=0;o<36;o++)n[o]||(s=0|16*Math.random(),n[o]=i[19==o?3&s|8:s])}return n.join("")}function filterXss(e){return e?e.replace(/\</g,"&lt;").replace(/\>/g,"&gt;"):e}var UA=window.navigator.userAgent,isIE,isWebkit,isTouch=!1;if((UA.indexOf("Edge/")>-1||UA.indexOf("MSIE ")>-1||UA.indexOf("Trident/")>-1)&&(isIE=!0),"ontouchstart"in window){var isTouch=!0;document.addEventListener("touchstart",function(){},!1)}var loadScript=function(e){var t,o;if(e&&""!=e)for(t=e.split(","),o=0;o<t.length;o++)$.getScript(t[o])},cookie={get:function(e){var t,o=new RegExp("(^| )"+e+"=([^;]*)(;|$)");return(t=document.cookie.match(o))?unescape(t[2]):null},set:function(e,t,o){if(o){var i=new Date;i.setMinutes(o),document.cookie=e+"="+encodeURIComponent(t)+";expires="+i.toGMTString()}else document.cookie=e+"="+encodeURIComponent(t)},clearcookie:function(e){document.cookie=e+"=;expires="+new Date(0).toGMTString()}},PAGE_ACTIVITY=!0;!function(){function e(e){var o={focus:!0,focusin:!0,pageshow:!0,blur:!1,focusout:!1,pagehide:!1};e=e||window.event,PAGE_ACTIVITY=e.type in o?o[e.type]:!this[t]}var t="hidden";t in document?document.addEventListener("visibilitychange",e):(t="mozHidden")in document?document.addEventListener("mozvisibilitychange",e):(t="webkitHidden")in document?document.addEventListener("webkitvisibilitychange",e):(t="msHidden")in document?document.addEventListener("msvisibilitychange",e):"onfocusin"in document?document.onfocusin=document.onfocusout=e:window.onpageshow=window.onpagehide=window.onfocus=window.onblur=e}(),window.INTERFACE_URLS={homeUrl:"/",logoutUrl:"/logout/",chatProtoUrl:"/v2/web/boss/js/module/chat.proto"},require(["module/search","module/detail","plugins/jquery.slider","module/deliver"],function(){$(function(){function e(){var e=arguments;s<=n-1&&(i.eq(s).stop(!0).animate({width:"300px"},500).siblings().stop(!0).animate({width:"98px"},500),++s==n&&(s=0)),o=setTimeout(e.callee,5e3)}function t(){var e=(r.offset().top,$(window).scrollTop(),$("body").outerHeight(),l.height(),$(window).height()-($("#footer").offset().top-$(document).scrollTop()));e>0?a.css("bottom",e):a.css("bottom",0)}if(Search.init(),Detail.init(),Deliver.init(),$.fn.hoverDelay=function(e){var t,o,i={hoverDuring:200,outDuring:200,hoverEvent:function(){$.noop()},outEvent:function(){$.noop()}},n=$.extend(i,e||{});return $(this).each(function(){$(this).hover(function(){clearTimeout(o),t=setTimeout(n.hoverEvent,n.hoverDuring)},function(){clearTimeout(t),o=setTimeout(n.outEvent,n.outDuring)})})},$(".home-box .slider-main").length&&($(".home-box .slider-main").hwSlider({autoPlay:!0,arrShow:!0,dotShow:!0,navShow:!0,touch:!0,height:240,interval:5e3,effect:"fade"}),$(".slider-box .pic-all").length)){var o,i=$(".slider-box .pic-all a"),n=i.length,s=0;i.hover(function(){clearTimeout(o),300!=$(this).width()&&$(this).stop(!0).animate({width:"300px"},500).siblings().stop(!0).animate({width:"98px"},500)},function(){s=$(this).index(),e()}),e()}if($(".semwrap .slider-main").length&&$(".slider-main").hwSlider({autoPlay:!0,arrShow:!0,dotShow:!1,navShow:!0,touch:!0,interval:5e3,width:582,speed:1e3,height:426}),$(".manager-list .manager-inner").length&&$(".manager-list li").length>1&&($(".manager-list h3").css("background","none"),$(".manager-list .manager-inner").hwSlider({autoPlay:!0,arrShow:!1,dotShow:!0,interval:5e3,speed:500,width:330,height:163,navShow:!0,touch:!0,effect:"fade",fadeOut:!1,afterSlider:function(){$(".manager-list .fold-text").removeAttr("style"),$(".manager-list .more-view").html('...展开<i class="fz fz-slidedown"></i></a>').show()}})),$(".picture-list .slider-main").length&&$(".picture-list li").length>1&&$(".picture-list .slider-main").hwSlider({autoPlay:!0,arrShow:!1,dotShow:!0,interval:5e3,speed:500,width:330,height:165,navShow:!0,touch:!0}),$(".job-menu dl").each(function(e){var t=$(this);t.hoverDelay({hoverDuring:200,hoverEvent:function(){switch(t.addClass("cur"),e){case 0:break;case 1:t.children(".menu-sub").css({top:"-50px"});break;case 10:t.children(".menu-sub").css({top:"auto",bottom:"-1px"})}if(0!=e&&1!=e&&10!=e||10==e&&$(".ie7").length){var o=t.get(0).getBoundingClientRect().top,i=t.find(".menu-sub");i.height()<o?i.css({"margin-top":65-i.height()+"px"}):o<70&&o>0?i.css({"margin-top":"-1px"}):o<0?i.css({"margin-top":o+"px"}):i.css({"margin-top":59-o+"px"})}},outEvent:function(){t.removeClass("cur").children(".menu-sub")}})}),$(".menu-all .sub-tab li").eq(0).css({"border-top-color":"#fff","padding-top":"15px","padding-bottom":"14px"}),$(".menu-all .sub-tab li").eq(1).css({"margin-top":"-1px"}),$(".menu-all .sub-tab li").on("click",function(){var e=$(this).index(),t=$(this).parent().find("li"),o=$(this).closest(".menu-sub").find(".sub-content ul");t.removeClass("cur"),$(this).addClass("cur"),o.removeClass("show"),o.eq(e).addClass("show"),0==e&&$(this).css("border-top-color","#fff"),e==t.length-1?$(this).css({"border-bottom-color":"#fff","margin-top":"-1px","padding-top":"1px"}):t.eq(t.length-1).css({"border-bottom-color":"#FDFDFE","margin-top":"0","padding-top":"0"})}),$(".condition-insdustry .btn-all").on("click",function(){$(this).parent().toggleClass("show-all-insdustry")}),$(".condition-city .link-district").on("click",function(){$(".condition-district").toggleClass("show-condition-district"),$(".condition-area").removeClass("show-condition-area")}),$(".condition-city .link-area").on("click",function(){$(".condition-area").toggleClass("show-condition-area"),$(".condition-district").removeClass("show-condition-district")}),$(".siderbar-top").on("click",function(){$("html,body").animate({scrollTop:"0px"},400)}),$(window).on("scroll",function(){$(this).scrollTop()>600?$("#siderbar").fadeIn():$("#siderbar").hide()}),$(".footer-scan").length){$("#siderbar").css({bottom:"304px",transition:"all 0.2s"});var r=$("#footer"),a=$(".footer-scan"),c=$(".home-box .job-list"),l=$(window);c.css("margin-bottom","105px"),t(),$(window).scroll(function(){t()}),a.find(".footer-scan-close").click(function(){a.fadeOut(300,function(){c.css({"margin-bottom":"15px",transition:"all 0.2s"}),$("#siderbar").css({bottom:"214px",transition:"all 0.2s"})})})}$(window).width()<1348&&$(".footer-scan .btns").css("margin-right","84px"),$(window).resize(function(){$(window).width()<1348?$(".footer-scan .btns").css("margin-right","84px"):$(".footer-scan .btns").css("margin-right","0")}),$(".ipt-wrap").find("input").focus(function(){$(".search-form form").addClass("search-form-shadow"),$(".ipt-wrap").addClass("ipt-wrap-hover"),$(".city-sel").addClass("city-sel-hover")}),$(".ipt-wrap").find("input").blur(function(){$(".search-form form").removeClass("search-form-shadow"),$(".ipt-wrap").removeClass("ipt-wrap-hover"),$(".city-sel").removeClass("city-sel-hover")})})}),require(["../../boss/js/plugins/jquery-confirm","module/sign","plugins/placeholder"],function(){$(".sign-wrap").length&&$(".sign-wrap").is(":visible")&&Sign.init(),PlaceholderCheck.init()}),$(".standard").length&&$(".nav-figure").length?require(["plugins/modernizr-custom","../../boss/js/module/chat-long","../../boss/js/module/chat-bytebuffer","../../boss/js/module/chat-protobuf","../../boss/js/module/chat-mqttws31","../../boss/js/module/chat-protobuf-message","../../boss/js/module/chat-emotion","../../boss/js/module/chat-publisher","../../boss/js/module/chat-notice","module/chat"],function(){Chat.init()}):$(".nav-figure").length&&($(".user-nav a").eq(0).attr("disabled","disabled"),$(".user-nav a").eq(0).on("click",function(e){alert("请升级您的浏览器才能使用聊天功能"),e.preventDefault()}),$(".chat-list").length&&$(".chat-list").html('<div class="data-tips"><div class="data-blank"><i class="tip-errordata"></i><b>请升级您的浏览器才能使用聊天功能</b></div></div>'),$(".boss-list").length&&$(".boss-list .data-tips").html('<div class="data-blank"><i class="tip-errordata"></i><b>请升级您的浏览器才能使用聊天功能</b></div>').show()),($(".resume").length||$(".job-detail").length)&&require(["../../boss/js/plugins/jquery-datetimepicker","../../boss/js/plugins/jquery.fileupload","/v2/chat_v2/js/pages/user_info.js","module/forms-validate","module/forms-ui","module/forms-data","module/resume"],function(){Resume.init(),FormsUI.init()});