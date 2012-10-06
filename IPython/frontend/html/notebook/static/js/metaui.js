//----------------------------------------------------------------------------
//  Copyright (C) 2012  The IPython Development Team
//
//  Distributed under the terms of the BSD License.  The full license is in
//  the file COPYING, distributed as part of this software.
//----------------------------------------------------------------------------

//============================================================================
// MetaUI
//============================================================================

var IPython = (function (IPython) {
    "use strict";


    var MetaUI = function (cell) {
        this.subelements = [];
        this.metainner = $('<div/>');
        this.cell = cell;
        this._update_array = [];
        var that = this;
        this.element = $('<div/>').addClass('metaedit')
                .append(this.metainner)
        //this.fadeI();
        this.add_raw_edit_button();
        var slide_s = MetaUI.slide_start({false:'Nothing Special',true:'Slide Start'})
        this.add_button(
            slide_s.init,
            slide_s.click,
            slide_s.update
            );
        slide_s = MetaUI.slide_step({false:'No step',true:'Is Step'})
        this.add_button(
            slide_s.init,
            slide_s.click,
            slide_s.update
            );

        return this;
    };

    MetaUI.prototype.raw_edit = function(md){

        var textarea = $('<textarea/>')
            .attr('rows','13')
            .attr('cols','75')
            .attr('name','metadata')
            .text(JSON.stringify(this.cell.metadata, null,4)||'');
        this.dialogform = $('<div/>').attr('title','Edit the metadata')
            .append(
                $('<form/>').append(
                    $('<fieldset/>').append(
                        $('<label/>')
                        .attr('for','metadata')
                        .text("Metadata (I know what I'm dooing and I won't complain if it breaks my notebook)")
                        )
                        .append($('<br/>'))
                        .append(
                            textarea
                        )
                    )
            );
        var editor = CodeMirror.fromTextArea(textarea[0], {
            lineNumbers: true,
            matchBrackets: true,
        });
        var that = this;
        $(this.dialogform).dialog({
                autoOpen: true,
                height: 300,
                width: 650,
                modal: true,
                buttons: {
                    "Ok": function() {
                        //validate json and set it
                        try {
                           var json = JSON.parse(editor.getValue());
                           that.cell.metadata = json;
                           $( this ).dialog( "close" );
                        }
                        catch(e)
                        {
                           alert('invalid json');
                        }
                    },
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    }
                },
                close: function() {
                    //cleanup on close
                    $(this).remove();
                }
        });
        editor.refresh();
        this.cell.unselect();
    }

    MetaUI.prototype.add_raw_edit_button = function() {
        var button_container = $('<div/>').addClass('button_container')
        var that = this;
        var button = $('<div/>').button({label:'Raw Edit'})
                .click(function(){that.raw_edit(); return false;})
        button_container.append(button);
        this.subelements.push(button_container);
        this.metainner.append(button_container);
    }

    //
    MetaUI.prototype.add_button = function (init_callback,click_callback,update_callback) {
       var button_container = $('<div/>').addClass('button_container');
       var that = this;
       var button =  $('<div/>').button({label:'None'})
           button.click(function(){
               click_callback(button,that.cell);
            });
       init_callback(button, this.cell);
       button_container.append(button)
       var that = this; 
       this._update_array.push(function(){update_callback(button, that.cell)})
       this.update();
       this.subelements.push(button_container);
       this.metainner.append(button_container);
       return button
    }

    MetaUI.prototype.update = function(){
        for( var v in this._update_array){
            this._update_array[v]()
        }
    }

    
    MetaUI.slide_start = function(dict){
       
        var  update = function(button,cell){
            try{
                $(button).button("option", "label", dict[cell.metadata.slideshow.slide_start]);
            }catch(e){}
        };

        var init = function(button,cell){
            if (cell.metadata.slideshow == undefined) {
                cell.metadata.slideshow = {}
            }
            update(button,cell)
         };
        
        var click = function(button, cell){
            cell.metadata.slideshow.slide_start = !cell.metadata.slideshow.slide_start;
            update(button,cell)
        };

       return {init:init, click:click, update:update}
    }


    MetaUI.slide_step = function(dict){
       
        var  update = function(button,cell){
            try{
                $(button).button("option", "label", dict[cell.metadata.slideshow.slide_step]);
            }catch(e){}
        };

        var init = function(button,cell){
            if (cell.metadata.slideshow == undefined) {
                cell.metadata.slideshow = {}
            }
            update(button,cell)
         };
        
        var click = function(button, cell){
            cell.metadata.slideshow.slide_step = !cell.metadata.slideshow.slide_step;
            update(button,cell)
        };

       return {init:init, click:click, update:update}
    }



    IPython.MetaUI = MetaUI;

    return IPython;
}(IPython));
