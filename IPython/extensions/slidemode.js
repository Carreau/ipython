/*
 * create an invisible input field that allows to get keyboard input
 * in order to control slide with keyboard
 */
var bind_remote = function(selector){
    var slide_control_input = $('<input/>')
        .attr('id','slide_control_input')
        .fadeTo(0.1,0)
        /*
         * bind the keyevent when slide control is enabled
         */
        .keydown(
                function(event){
                        if(event.which == IPython.utils.keycodes.LEFT_ARROW){
                            IPython.slideshow.prev();
                        }
                        else if(event.which == IPython.utils.keycodes.RIGHT_ARROW){
                            IPython.slideshow.next();
                        }
                    event.preventDefault();
                    return false;
            })
         /*
          * Modifie the state of the button that allows to take slide control when
          * slide_control_input get in/out of focus
          */
         .focusin(function(){$('#slide_control_button').button('option','label','Slide Control Enabled')})
         .focusout(function(){$('#slide_control_button').button('option','label','Enable Slide Control')})

        var slide_control_button = $('<div/>')
            .attr('id','slide_control_button')
            .button({label:'Enable Slide Control'})
            .attr('style','float:right')
            .click(
                function(){
                    $('#slide_control_input').focus();
                })
    var hin = function(){$(selector).fadeTo('slow',1);}
    var hout= function(){$(selector).fadeTo('slow',0.3);}

    // this will make the toolbar translucent on top of the screen
    // which will fade-in on hover
    $(selector)
        .append(slide_control_input)
        .append(slide_control_button)
        .fadeTo('slow',0.3)
    .hover(hin,hout)

}

/* this is still a prototype, but should allow to progressively show a code cell.
var show_line = function(cell,line_number){
    cell.code_mirror.showLine(cell.code_mirror.getLineHandle(line_number-1))    }
*/


IPython = (function(IPython) {

    var Presentation = function(){
        // ccell == current cell number
        this.ccell = 0;
    }

    var is_new_slide_beginning = function(cell){
        return (cell.metadata.slideshow.slide_start)
    }

    // we need the ability to create a presentation toolbar
    // that show diverse slide actions
    Presentation.prototype.create_toolbar = function(){
        var that = this;
        var presentation_toolbar_div = $('<div/>').attr('id','toolbar_present').addClass('toolbar');
        // eta is estimated time of arrival
        // this is just a button with `current slide/ number of slides`
        this.avancement = $('<div/>').button({label:that.eta()});
        presentation_toolbar_div.append(this.avancement);

        // append it juste after the main toolbar
        $('#maintoolbar').after(presentation_toolbar_div);
        var ptoolbar = new IPython.ToolBar('#toolbar_present');
        IPython.ptoolbar = ptoolbar;
        ptoolbar.add_buttons_group([{label:'Pause', icon:'ui-icon-pause', callback:function(){that.stop()}}])
        ptoolbar.add_buttons_group([{label:'Stop', icon:'ui-icon-stop', callback:function(){that.restart();that.stop()}}])
        ptoolbar.add_buttons_group([
            {label:'Restart from 0', icon:'ui-icon-arrowthickstop-1-w', callback:function(){that.stop(); that.restart(); that.start()}}
            ])
        ptoolbar.add_buttons_group([
            {label:'Prev Slide', icon:'ui-icon-seek-prev', callback:function(){that.prev_group()}},
            {label:'Next Slide', icon:'ui-icon-seek-next', callback:function(){that.next_group()}},
            ])
        ptoolbar.add_buttons_group([
            {label:'Step Next', icon:'ui-icon-play', callback:function(){that.next()}}
            ])
        
        // add ability to switch focus btween slide control and classic nb control
        bind_remote('#toolbar_present');
    }

    Presentation.prototype.remove_toolbar = function(){
        $('#toolbar_present').remove();
    }

        
    Presentation.prototype.nslides = function(){
        var cells = IPython.notebook.get_cells();
        var cnt =0
        for( var i=0; i< cells.length;i++)
            if(is_new_slide_beginning(cells[i])) cnt++;
        return cnt
    }

    Presentation.prototype.n_current_slide = function(){
        var cells = IPython.notebook.get_cells();
        var cnt =0
        for( var i=0; i<= this.ccell ;i++)
            if(is_new_slide_beginning(cells[i])) cnt++;
        return cnt
    }

    Presentation.prototype.eta = function(){
        return this.n_current_slide()+'/'+this.nslides()
    }

    Presentation.prototype.next_marked_cell_n = function() {
        for(var i=this.ccell+1; i< $('.cell').length; i++) {
            if(is_new_slide_beginning(IPython.notebook.get_cell(i)))
            { return i; }
        }
        return null;
    }

    Presentation.prototype.prev_marked_cell_n = function() {
        for(var i=this.ccell-1; i> 0; i--) {
            if(is_new_slide_beginning(IPython.notebook.get_cell(i))){
                    return i
            }
        }
        return 0;
      }

      // restart a presentation from slide 0
      Presentation.prototype.start = function(){
            this.restart();
            this.resume();
      }

      // make the current avancement to 0
      Presentation.prototype.restart = function(){
            this.ccell = 0;
            $(this.avancement).remove();
            delete this.avancement;
      }

      // start a presentation fromo where you left off
      Presentation.prototype.resume = function(){
            this.create_toolbar();
            $('#menubar, #pager_splitter, #pager, #header,#maintoolbar').addClass('pmode');
            $('.cell').fadeOut();
            if(this.current_is_marked()){
                $('.cell:nth('+this.ccell+')').fadeIn();
            } else {
                for( var i=this.prev_marked_cell_n() ; i<= this.ccell; i++){
                    $('.cell:nth('+i+')').fadeIn();
                }
            }
            var that=this;
            if(this.avancement != undefined){
                $(this.avancement).button('option','label',that.eta())
            }
            setTimeout(function(){IPython.layout_manager.do_resize();},1000);
            return this;
      }

      Presentation.prototype.stop = function(){
          $('.cell').fadeIn();
          $('.pmode').removeClass('pmode');
          $('div#notebook').removeClass('pove');
          this.remove_toolbar();
      }

      Presentation.prototype.next = function(){
          this.ccell = this.ccell+1;
          var that = this;
          if(this.ccell >= $('.cell').length ){
              this.restart();
              this.stop();
              return;
          }
          var nnext = this.ccell;
          var ncell = IPython.notebook.get_cell(nnext)

          if(is_new_slide_beginning(ncell)){
              $('.cell').fadeOut(100);
              setTimeout(function(){$('.cell:nth('+nnext+')').fadeIn(100)},150);
          } else {
              setTimeout(function(){$('.cell:nth('+nnext+')').fadeIn(200)},0);
          }
          $(this.avancement).button('option','label',that.eta())
          setTimeout(function(){IPython.layout_manager.do_resize();},1000);
          return this;
      }

      Presentation.prototype.next_group = function(){
          this.ccell = this.next_marked_cell_n();
          var that = this;
          $('.cell').fadeOut(100);
          setTimeout(function(){
              $('.cell:nth('+that.ccell+')').fadeIn(100)
                  },150);
          setTimeout(function(){IPython.layout_manager.do_resize();},1000);
          $(this.avancement).button('option','label',that.eta())
      }

      Presentation.prototype.prev_group = function(){
          this.ccell = this.prev_marked_cell_n();
          var that = this
          $('.cell').fadeOut(100);
          setTimeout(function(){$('.cell:nth('+that.ccell+')').fadeIn(100)},150);
          $(this.avancement).button('option','label',that.eta())
      }

      Presentation.prototype.is_n_marked = function(n){
          return is_new_slide_beginning(IPython.notebook.get_cell(n))
      }

      Presentation.prototype.current_is_marked = function(n){
          return is_new_slide_beginning(IPython.notebook.get_cell(this.ccell));
      }

      Presentation.prototype.prev = function(){
          if(is_new_slide_beginning(IPython.notebook.get_cell(this.ccell))){
              var pmcell = this.prev_marked_cell_n();
              $('.cell').fadeOut(100);
              for( var i=pmcell; i< this.ccell ; i++ ){
                  (function(val){
                      return function(){
                                  setTimeout( function(){
                                      $('.cell:nth('+val+')').fadeIn(100)
                                      },150);
                      }
                   })(i)();
              }
          } else {
              $('.cell:nth('+this.ccell+')').fadeOut(200);
          }
          this.ccell = this.ccell -1;
          return this;
      }

      IPython.Presentation = Presentation;
      return IPython;

    })(IPython);

    $('body').append($('<style/>').text('.pmode{ display: none !important }'));
    IPython.slideshow = new IPython.Presentation();

    var sid = 'start_pmode'
    if(($('#'+sid)).length == 0) {
          IPython.toolbar.add_buttons_group([
                  {'label'  :'Start Slideshow',
                    'icon'  :'ui-icon-image',
                    'callback':function(){IPython.slideshow.resume()},'id':sid},
              ])
         }
