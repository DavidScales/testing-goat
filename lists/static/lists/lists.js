window.Superlists = {};
window.Superlists.initialize = () => {
  $('input[name="text"]').on('keypress', function () {
    $('.has-error').hide();
  });
};