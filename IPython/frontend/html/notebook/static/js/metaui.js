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
        this.element = $('<div/>').addClass('metaedit2')
                .append(this.metainner)
        //this.fadeI();
        this.add_raw_edit_button();
        this.add_button('bt1',['Group Stop','Slide Stop','Show With Previous',"Never Show"]);
        this.add_button('bt2',['In & Out','In / Out','In Only','Out Only']);
        //this.add_button('bt3',['button ---','button +++','button ===']);
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
        this.cell.unselect();
        editor.refresh();
    }

    MetaUI.prototype.add_raw_edit_button = function() {
        var button_container = $('<div/>').addClass('bc')
        var that = this;
        var button = $('<div/>').button({label:'Raw Edit'})
                .click(function(){that.raw_edit()})
        button_container.append(button);
        this.subelements.push(button_container);
        this.metainner.append(button_container);
    }

    MetaUI.prototype.add_button = function (subkey,labels) {
       var labels = labels || ["on","off"];
       var that = this;
       var bc = $('<div/>').addClass('bc');
       var button =  $('<div/>').button({label:labels[0]})
           button.value = 0;
           button.click(function(){
               button.value = (button.value+1)% labels.length || 0;
               button.sticky = (button.value != 0);
               that.cell.metadata[subkey] = labels[button.value];
               $(button).button( "option", "label",labels[button.value]);
            });
       bc.append(button)
       this.subelements.push(bc);
       this.metainner.append(bc);
       return button
    }


    IPython.MetaUI = MetaUI;

    return IPython;
}(IPython));
