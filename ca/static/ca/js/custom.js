/**
 * Created by mefesto on 24.05.17.
 */
$(document).ready(function () {
   $('#files-upload').click(function () {
      $('#first-textarea').hide();
      $('#second-textarea').hide();
      $('#first-input-button').show();
      $('#second-input-button').show();
   });
   $('#textareas-upload').click(function () {
      $('#first-textarea').show();
      $('#second-textarea').show();
      $('#first-input-button').hide();
      $('#second-input-button').hide();
   });

   new Clipboard('#copy-to-clipboard');

});