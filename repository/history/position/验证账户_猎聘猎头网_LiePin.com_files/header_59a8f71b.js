!function($){var HeaderHelper=function(){return this.option={showMessagePops:!0},this.quickMenu=$("header .quick-menu"),this.config=window.HeaderHelperConfig||{},this.init(),this};HeaderHelper.prototype.init=function(){var that=this;return LT.Event.queue("login",function(){LT.User.get(),that.refresh()}),this.refresh(),this},HeaderHelper.prototype.options=function(){var that=this;return 1===arguments.length?that.option[arguments[0]]:(2===arguments.length&&(that.option[arguments[0]]=arguments[1]),this)},HeaderHelper.prototype.refresh=function(){var alishost=location.hostname.split(".").slice(0,1)[0];switch(alishost){case"clt":case"ltcom":LT.Cookie.get("hcomp_id")?this.setLoginedMenuCLT():this.setUnloginMenuCLT();break;default:LT.User.isLogin?this.setLoginedMenu():this.setUnloginMenu()}return this},HeaderHelper.prototype.setUnloginMenu=function(){var that=this,quickMenu=$("<div />").addClass("quick-menu-unlogined").appendTo(that.quickMenu.empty());return NodeTpl.get("//concat.lietou-static.com/dev/passport/pc/revs/v1/tpls/header/www_quick_menu_c1f68d1b.js",{pageType:that.config.pageType},function(d){quickMenu.append(d)}),that},HeaderHelper.prototype.setLoginedMenu=function(){switch(LT.User.user_kind){case"0":this.setLoginedMenuC();break;case"2":this.setLoginedMenuH();break;default:this.setLoginedMenuP()}return this},HeaderHelper.prototype.setLoginedMenuC=function(){var that=this,quickMenu=$("<div />").addClass("quick-menu-logined-c").appendTo(that.quickMenu.empty());return NodeTpl.get("//concat.lietou-static.com/dev/passport/pc/revs/v1/tpls/header/c_quick_menu_92f50066.js",function(d){quickMenu.append(d)}),that},HeaderHelper.prototype.setLoginedMenuH=function(){var that=this,quickMenu=$("<div />").addClass("quick-menu-logined-h").appendTo(that.quickMenu.empty());return NodeTpl.get("//concat.lietou-static.com/dev/passport/pc/revs/v1/tpls/header/h_quick_menu_ce827652.js",function(d){quickMenu.append(d)}),that},HeaderHelper.prototype.setUnloginMenuCLT=function(){var that=this,quickMenu=$("<div />").addClass("quick-menu-unlogined").appendTo(that.quickMenu.empty());return NodeTpl.get("//concat.lietou-static.com/dev/passport/pc/revs/v1/tpls/header/clt_quick_menu_unlogined_9ad0493c.js",function(d){quickMenu.append(d)}),$("header .notebook").remove(),that},HeaderHelper.prototype.setLoginedMenuCLT=function(){var that=this,quickMenu=$("<div />").addClass("quick-menu-logined-clt").appendTo(that.quickMenu.empty()),isroot=1==LT.Cookie.get("is_root_hcomp"),compname=LT.Cookie.get("hcomp_name");return NodeTpl.get("//concat.lietou-static.com/dev/passport/pc/revs/v1/tpls/header/clt_quick_menu_ecbf70d5.js",{isroot:isroot},function(d){quickMenu.append(d)}),compname?($("header nav").show(),$("header .title").hide()):($("header nav").hide(),$("header .title").show()),that},HeaderHelper.prototype.setLoginedMenuP=function(){var that=this,quickMenu=$("<div />").addClass("quick-menu-logined-p").appendTo(that.quickMenu.empty());return NodeTpl.get("//concat.lietou-static.com/dev/passport/pc/revs/v1/tpls/header/p_quick_menu_2c0c845b.js",function(d){quickMenu.append(d)}),that},HeaderHelper.prototype.navbar=function(name){return $("header nav ul li").each(function(){$(this).attr("data-name")===name&&$(this).addClass("active")}),this},HeaderHelper.prototype.dynmode=function(name){return LT.User.isLogin&&$("header nav").hide(),this},window.HeaderHelper=new HeaderHelper}(jQuery);