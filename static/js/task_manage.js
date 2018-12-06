$(document).ready(function() {
  $('.btn-add-todo').on('click', function(e) {
      e.preventDefault();

      var total_forms = parseInt($('#id_form-TOTAL_FORMS').val());
      $('#id_form-TOTAL_FORMS').val(total_forms + 1);

      var html =
      '<div class="row"> \
        <div class="col-md-8"> \
            <div class="form-group is-valid"> \
            <label class="sr-only" for="id_form-' + total_forms + '-description">Description</label> \
            <textarea name="form-' + total_forms + '-description" cols="40" rows="10" class="form-control is-valid" placeholder="Description" title="" id="id_form-' + total_forms + '-description"></textarea> \
            </div> \
        </div> \
        <div class="col-md-4"> \
            <div class="form-group is-valid"> \
              <label class="sr-only" for="id_form-' + total_forms + '-images">Images</label> \
              <div class="row bootstrap4-multi-input"> \
                <div class="col-12"> \
                  <input type="file" name="form-' + total_forms + '-images" multiple="" class="is-valid" title="" id="id_form-' + total_forms + '-images"> \
                </div> \
              </div> \
            </div> \
        </div> \
      </div>';

      $('.todo-formset .forms').append(html);
  });
});
