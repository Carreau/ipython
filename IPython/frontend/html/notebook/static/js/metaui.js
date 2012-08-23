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
        var metawrapper = $('<div/>').addClass('metaedit2')
                .append(this.metainner)
        this.fadeI();
        this.add_button('bt1',['Group Stop','Slide Stop','Show With Previous',"Never Show"]);
        this.add_button('bt2',['In & Out','In / Out','In Only','Out Only']);
        //this.add_button('bt3',['button ---','button +++','button ===']);
        return this;//metawrapper;
    };
   
    MetaUI.prototype.raw_edit = function(md){

        var ta = $('<textarea/>')
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
                        .text('Metadata')
                        )
                        .append($('<br/>'))
                        .append(
                            ta
                        )
                    )
                
            );
        $(this.dialogform).dialog({
                autoOpen: true,
                height: 300,
                width: 650,
                modal: true
        });
        var editor = CodeMirror.fromTextArea(ta[0], {
            lineNumbers: true,
            matchBrackets: true,
        });
        this.cell.unselect();
    }


    MetaUI.prototype.fadeO = function(){
        //fadeout all inner element unless they are sticky
        this.cell.metadata.test = 1;
        var sb = this.subelements;
        for(var i in sb){
            if(sb[i].sticky != true){
                $(sb[i]).fadeTo("fast",0)
            }
        }
    }

    MetaUI.prototype.fadeI = function(){
        //FadeIn all elements
        for(var i in this.subelements){
            this.subelements[i].fadeTo("fast",1)
        }
    }



    MetaUI.prototype.add_button = function (sk,labels) {
       var labels = labels || ["on","off"]
       var that = this;
       var bc = $('<div/>').addClass('bc');
       var button =  $('<div/>').button({label:labels[0]})
           button.value = 0;
           button.click(function(){
               button.value = (button.value+1)% labels.length || 0;
               button.sticky = (button.value != 0);
               that.cell.metadata[sk] = labels[button.value];
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
