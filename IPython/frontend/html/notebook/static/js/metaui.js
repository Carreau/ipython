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
        var that = this;
        this.element = $('<div/>').addClass('metaedit')
                .append(this.metainner)
        //this.fadeI();
        this.add_raw_edit_button();
        this.add_button(
            MetaUI.cycle_init_helper({false:'Nothing Special',true:'Slide Start'}),
            MetaUI.cycle_helper({false:'Nothing Special',true:'Slide Start'})
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
    MetaUI.prototype.add_button = function (init_callback,click_callback) {
       var button_container = $('<div/>').addClass('button_container');
       var that = this;
       var button =  $('<div/>').button({label:'None'})
           button.click(function(){
               click_callback(button,that.cell);
            });
       init_callback(button, this.cell);
       button_container.append(button)
       var that = this; 
       var lup = MetaUI.cycle_update_helper({false:'Nothing Special',true:'Slide Start'});
       this.update = function(){lup(button, that.cell)};
       this.subelements.push(button_container);
       this.metainner.append(button_container);
       return button
    }

    
    MetaUI.cycle_update_helper = function(dict) {
        return function(button,cell){
            $(button).button( "option", "label", dict[cell.metadata.slideshow.slide_start]);
        }
    }

    MetaUI.cycle_init_helper = function(dict) {
        return function(button,cell){
            $(button).button( "option", "label",'inited'); 
            if (cell.metadata.slideshow == undefined) {
                 cell.metadata.slideshow = {}
            }
            $(button).button( "option", "label", dict[cell.metadata.slideshow.slide_start]);
        }
    }


    MetaUI.cycle_helper = function(dict){
         return  function(button, cell){
            cell.metadata.slideshow.slide_start = !cell.metadata.slideshow.slide_start;
            $(button).button( "option", "label", dict[cell.metadata.slideshow.slide_start]);
        }
    }

    IPython.MetaUI = MetaUI;

    return IPython;
}(IPython));
