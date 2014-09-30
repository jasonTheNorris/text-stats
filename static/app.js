$(function() {
  var TextStats = function() {
    var self = this;

    this.$editor = $('.editor');
    this.$calculateButton = $('.header .calculate');
    this.$backButton = $('.header .back');
    this.$stats = $('.stats')

    this.statsTableTemplate = $('.stats-table-template').html();
    Mustache.parse(self.statsTableTemplate);

    this.$editor.focus().on('keyup', function() {
      if (self.$editor.val()) {
        self.$calculateButton.fadeIn();
      } else {
        self.$calculateButton.fadeOut();
      }
    });

    self.$calculateButton.on('click', function() {
      self.toggleCalculateButton(true);
      $.post('/api/calculate', { text: self.$editor.val() }, function(respData) {
        var data = respData;
        self.$editor.fadeOut(function() {
          self.$calculateButton.fadeOut(function() {
            self.toggleCalculateButton(false);
            self.$backButton.fadeIn();
          });
          self.renderStats(data);
        });
      });
    });

    self.$backButton.on('click', function() {
      self.$stats.fadeOut(function() {
        self.$backButton.fadeOut(function() {
          self.$calculateButton.fadeIn();
        });
        self.$editor.fadeIn();
      });
    });
  };

  TextStats.prototype.renderStats = function(data) {
    var self = this;
    var statsTableHtml = Mustache.render(this.statsTableTemplate, data);
    this.$stats.html(statsTableHtml).fadeIn();
  };

  TextStats.prototype.toggleCalculateButton = function(isCalculating) {
    if (isCalculating) {
      this.$calculateButton.attr('disabled', true).text('Calculating...');
    } else {
      this.$calculateButton.removeAttr('disabled').text('Calculate');
    }
  };

  var textStats = new TextStats();
});
