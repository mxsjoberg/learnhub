$(document).ready(function() {
    /* Stripe
    ------------------------------------------------------- */
    var stripe = Stripe('pk_live_BpvLaK6nbAXUGf3Cn1Vbl4x3', {
        betas: ['checkout_beta_4']
    });

    $("body").on('click', 'button.checkout-button', function () {
        var type = this.getAttribute('data-type');
        var sku = this.getAttribute('data-sku');

        // once or plan
        if (type == 'once') {
            stripe.redirectToCheckout({
                items: [{sku: sku, quantity: 1}],
                successUrl: 'https://learnhub.io/success',
                cancelUrl: 'https://learnhub.io/canceled',
            })
            .then(function (result) {
                if (result.error) {
                    var displayError = document.getElementById('error-message');
                    displayError.textContent = result.error.message;
                }
            });
        } else if (type == 'plan') {
            stripe.redirectToCheckout({
                items: [{plan: sku, quantity: 1}],
                successUrl: 'https://learnhub.io/success',
                cancelUrl: 'https://learnhub.io/canceled',
            })
            .then(function (result) {
                if (result.error) {
                    var displayError = document.getElementById('error-message');
                    displayError.textContent = result.error.message;
                }
            });
        }
    });

    /* Functions
    ------------------------------------------------------- */
    // get pinned pathways in localstorage
    var get_pinned_pathways = function() {
        var pinned_pathways = localStorage.getItem('pinned_pathways');
        if (!pinned_pathways) {
            // initialise
            pinned_pathways = []
            return pinned_pathways
        } else {
            return pinned_pathways.split(',');
        }
    };
    // notification function (similar to Flask flashes)
    var notification = function(message, category) {
        $('#notifications').append("\
            <div class='toast toast-" + category + " mt-2'>\
                <a class='btn btn-clear float-right notification close'></a>\
                " + message + "\
            </div>"
        );
    };
    // append to skill wrapper function
    var append_to_skill_wrapper = function(skill_id, skill_name, skill_level) {
        $('#skill_wrapper').append("\
        <div id='" + skill_id + "' class='column col-12'>\
            <div class='columns'>\
                <div class='column col-3 p-2'>\
                    <p class='m-0 pl-2'>" + skill_name + "</p>\
                </div>\
                <div class='column col-8 p-2'>\
                    <div class='bar'>\
                        <div class='bar-item' role='progressbar' style='width:" + skill_level + "%;' aria-valuenow='" + skill_level + "' aria-valuemin='0' aria-valuemax='100'></div>\
                    </div>\
                </div>\
                <div class='column col-1'>\
                    <button class='btn btn-link btn-block delete tooltip tooltip-left' data-tooltip='Remove skill: " + skill_name + "' type='submit' data-skill-id='" + skill_id + "'><i class='fas fa-minus-circle'></i></button>\
                </div>\
            </div>\
        </div>");
    };
    // append skill to project skills
    var append_to_project_skills = function(skill_id, skill_name) {
        
        $('#project_skills').append("<option value='" + skill_id + "'>" + skill_name + "</option>");
    };
    // update username
    var update_username = function(account_update_username) {
        var pattern = "[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$"
        // match input pattern
        if (account_update_username.match(pattern)) {
            $.getJSON($SCRIPT_ROOT + '/_account_update_username', {
                account_update_username: account_update_username
            }, function(data) {
                if (data.response == true) {
                    notification("Successfully updated username", "error");
                } else if (data.response == -1) {
                    notification("This username is already used.", "error");
                } else {
                    notification("Something went wrong.", "error");
                }
            });
        }
        else {
            notification("Invalid username.", "error");
        }
    };
    // update name
    var update_name = function(account_update_name) {
        var pattern = "[A-Za-z ]{1,32}$"
        // match input pattern
        if (account_update_name.match(pattern)) {
            $.getJSON($SCRIPT_ROOT + '/_account_update_name', {
                account_update_name: account_update_name
            }, function(data) {
                if (data.response == true) {
                    notification("Successfully updated name", "error");
                } else {
                    notification("Something went wrong.", "error");
                }
            });
        }
        else {
            notification("Invalid name.", "error");
        }
    };
    // update location
    var update_location = function(account_update_location) {
        var pattern = "[A-Za-z ]{1,32}$"
        // match input pattern
        if (account_update_location.match(pattern)) {
            $.getJSON($SCRIPT_ROOT + '/_account_update_location', {
                account_update_location: account_update_location
            }, function(data) {
                if (data.response == true) {
                    notification("Successfully updated location", "error");
                } else {
                    notification("Something went wrong.", "error");
                }
            });
        }
        else {
            notification("Invalid location.", "error");
        }
    };
    // update avatar
    var update_avatar = function(account_update_avatar) {
        var reader = new FileReader();
        reader.readAsDataURL(account_update_avatar);
        reader.onload = function () {
            var image = reader.result
            // check result
            if (image) {
                $.ajax({
                    //dataType: "json",
                    type: "POST",
                    url: $SCRIPT_ROOT + "/_account_update_avatar",
                    data: JSON.stringify(image, null, "\t"),
                    contentType: "application/json;charset=UTF-8",
                    success: function(response){
                        //console.log(response)
                        notification("Successfully updated avatar", "error");
                    },
                    error: function(response){
                        notification("Something went wrong.", "error");
                    }
                });
            }
            else {
                notification("Invalid file.", "error");
            }
        };
    };
    // update facebook
    var update_facebook = function(account_update_facebook) {
        $.getJSON($SCRIPT_ROOT + '/_account_update_facebook', {
            account_update_facebook: account_update_facebook
        }, function(data) {
            if (data.response == true) {
                notification("Successfully updated Facebook", "error");
            } else {
                notification("Something went wrong.", "error");
            }
        });
    };
    // update twitter
    var update_twitter = function(account_update_twitter) {
        $.getJSON($SCRIPT_ROOT + '/_account_update_twitter', {
            account_update_twitter: account_update_twitter
        }, function(data) {
            if (data.response == true) {
                notification("Successfully updated Twitter", "error");
            } else {
                notification("Something went wrong.", "error");
            }
        });
    };
    // update github
    var update_github = function(account_update_github) {
        $.getJSON($SCRIPT_ROOT + '/_account_update_github', {
            account_update_github: account_update_github
        }, function(data) {
            if (data.response == true) {
                notification("Successfully updated GitHub", "error");
            } else {
                notification("Something went wrong.", "error");
            }
        });
    };
    // create pathway
    var create_pathway = function(pathway_name, pathway_level, pathway_tags) {
        $.getJSON($SCRIPT_ROOT + '/_create_new_pathway', {
            pathway_name: pathway_name,
            pathway_level: pathway_level,
            pathway_tags: pathway_tags
        }, function(data) {
            if (data.response != false && data.response != -1) {
                var pathway_id = data.response
                console.log('Created pathway: ' + pathway_id)
                notification("Successfully created new pathway.", "error");
                location.reload();
            } else if (data.response == -1) {
                notification("Invalid pathway details.", "error");
            } else {
                notification("Something went wrong.", "error");
            }
        });
    };
    // add resource to pathway
    var add_resource = function(pathway_id, resource_name, resource_link, resource_type) {
        $.getJSON($SCRIPT_ROOT + '/_add_resource', {
            pathway_id: pathway_id,
            resource_name: resource_name,
            resource_link: resource_link,
            resource_type: resource_type
        }, function(data) {
            if (data.response == true) {
                console.log('Added resource: ' + resource_name)
                notification("Successfully added resource.", "error");
                location.reload();
            } else if (data.response == -1) {
                notification("Invalid resource name.", "error");
            } else if (data.response == -2) {
                notification("You are not owner.", "error");
            } else {
                notification("Something went wrong.", "error");
            }
        });
    };

    /* On load
    ------------------------------------------------------- */
    // initialize search
    $('#search').hideseek({
        attribute: 'data-search',
        ignore: '.search-ignore'
        // highlight: true
    });
    // initialise select2 on project_skills
    $('#project_skills.form-select.multiple').select2({
        placeholder: "Select skills",
        allowClear: true,
        tags: true
    });
    // initialise select2 on pathway_tags
    $('#pathway_tags.form-select.multiple').select2({
        placeholder: "Add tags",
        allowClear: true,
        tags: true,
        language: {
            noResults: function () {
                return "";
            }
        }
    });
    // initialise select2 on pathway_owners
    $('#pathway_owners.form-select.multiple').select2({
        allowClear: false,
        tags: true,
        language: {
            noResults: function () {
                return "";
            }
        }
    });
    // initialise select2 on edit_pathway_tags
    $('#edit_pathway_tags.form-select.multiple').select2({
        placeholder: "Add tags",
        allowClear: true,
        tags: true,
        language: {
            noResults: function () {
                return "";
            }
        }
    });
    // reset project name loading
    $('#project_name_icon').removeClass('loading');
    // reset skill name loading
    $('#skill_name_icon').removeClass('loading');
    // set pin button text based on pathway pinned or not
    var pinned_pathways = get_pinned_pathways();
    $('.button-pin').each(function() {
        var pathway_id = $(this).attr('data-pathway-id');
        //console.log(pathway_id)
        if (pinned_pathways.includes(pathway_id)) {
            $(this).text('Unpin');
        } else {
            $(this).text('Pin');
        }
    });
    // move pinned pathways to top
    $.each(pinned_pathways, function(index, value) {
        $("#" + value).prependTo('#pathways_wrapper_list');
        $("#" + value).addClass('search-ignore');
    });

    /* AJAX calls
    ------------------------------------------------------- */
    // AJAX add skill
    $("body").on('click', 'button#skill_submit', function () {
        $('#skill_name_icon').addClass('loading');

        // define skill
        var skill_name = $('input[name=skill_name]').val();
        var skill_level = $('select[name=skill_level]').val();

        $.getJSON($SCRIPT_ROOT + '/_add_skill', {
            skill_name: skill_name,
            skill_level: skill_level,
        }, function(data) {
            if (data.response != false && data.response != -1) {
                var skill_id = data.response

                // remove empty state
                $('#skill_empty').remove();

                // append to skill wrapper
                append_to_skill_wrapper(skill_id, skill_name, skill_level);
                console.log('Added skill id ' + skill_id + ' to skill wrapper.');

                // append to project skills
                append_to_project_skills(skill_id, skill_name);
                console.log('Added skill id ' + skill_id + ' to project skills.');
                
                // reset form inputs
                $('#skill_name_icon').removeClass('loading');
                $('input[name=skill_name]').val('');
                $('select[name=skill_level]').val('20');

            } else if (data.response == -1) {
                notification("You already added this skill.", "error");
                $('#skill_name_icon').removeClass('loading');
            } else {
                notification("Something went wrong.", "error");
                $('#skill_name_icon').removeClass('loading');
            }
        });
        return false;
    });
    // AJAX delete skill
    $("body").on('click', 'button.delete', function () {
        var skill_id = this.getAttribute('data-skill-id')

        $.getJSON($SCRIPT_ROOT + '/_delete_skill', {
            skill_id: skill_id
        }, function(data) {
            if (data.response == true) {
                // remove from skill wrapper
                $('#' + skill_id).remove();
                console.log('Removed skill id ' + skill_id + ' from skill wrapper.');

                // remove from project skills
                $('#project_skills option[value="' + skill_id + '"]').remove();
                console.log('Removed skill id ' + skill_id + ' from project skills.');
            } else {
                notification("Something went wrong.", "error");
            }
        });
        return false;
    });
    // AJAX add project
    $("body").on('click', 'button#project_submit', function () {
        $('#project_name_icon').addClass('loading');

        // define skill
        var project_name = $('input[name=project_name]').val();
        var project_description = $('textarea[name=project_description]').val();
        var project_link = $('input[name=project_link]').val();
        var project_skills = $('select[name=project_skills]').val();

        project_skills = project_skills.join()

        //console.log(project_description);

        $.getJSON($SCRIPT_ROOT + '/_add_project', {
            project_name: project_name,
            project_description: project_description,
            project_link: project_link,
            project_skills: project_skills
        }, function(data) {
            if (data.response != false && data.response != -1) {
                $('#projects_empty').remove();

                var project_id = data.response
                console.log('Added project id: ' + project_id);
                //$('#project_name_icon').removeClass('loading');
                // $('input[name=project_name]').val('');
                // $('input[name=project_link]').val('');
                // $('select[name=project_skills]').val(null).trigger('change');
                location.reload();

            } else if (data.response == -1) {
                notification("You already added this project.", "error");
                $('#project_name_icon').removeClass('loading');
            } else {
                notification("Something went wrong.", "error");
                $('#project_name_icon').removeClass('loading');
            }
        });
        return false;
    });
    // AJAX delete project
    $("body").on('click', 'button.delete-project', function () {
        var project_id = this.getAttribute('data-project-id')

        $.getJSON($SCRIPT_ROOT + '/_delete_project', {
            project_id: project_id
        }, function(data) {
            if (data.response == true) {
                $('#' + project_id).remove();
                console.log('Removed project id: ' + project_id);
            } else {
                notification("Something went wrong.", "error");
            }
        });
        return false;
    });
    // AJAX update account
    $("body").on('click', 'button[name=account_update_submit]', function () {
        var account_update_username = $('input[name=account_update_username]').val()
        var account_update_name = $('input[name=account_update_name]').val()
        var account_update_location = $('input[name=account_update_location]').val()
        var account_update_avatar = $('input[name=account_update_avatar]').prop('files')[0];
        var account_update_facebook = $('input[name=account_update_facebook]').val()
        var account_update_twitter = $('input[name=account_update_twitter]').val()
        var account_update_github = $('input[name=account_update_github]').val()

        // update_username
        if (account_update_username) {
            update_username(account_update_username);
            console.log('Updated username to: ' + account_update_username)
        }
        // update_name
        if (account_update_name) {
            update_name(account_update_name);
            console.log('Updated name to: ' + account_update_name)
        }
        // update_location
        if (account_update_location) {
            update_location(account_update_location);
            console.log('Updated location to: ' + account_update_location)
        }
        // update_avatar
        if (account_update_avatar) {
            update_avatar(account_update_avatar);
            console.log('Successfully updated avatar.')
        }
        // update_facebook
        if (account_update_facebook) {
            update_facebook(account_update_facebook);
            console.log('Successfully updated facebook to: ' + account_update_facebook)
        }
        // update_twitter
        if (account_update_twitter) {
            update_twitter(account_update_twitter);
            console.log('Successfully updated twitter: ' + account_update_twitter)
        }
        // update_github
        if (account_update_github) {
            update_github(account_update_github);
            console.log('Successfully updated github to: ' + account_update_github)
        }
        return false;
    });
    // AJAX create pathway
    $("body").on('click', 'button[name=create_new_pathway_submit]', function () {
        // pathway details
        var pathway_name = $('input[name=pathway_name]').val()
        var pathway_level = $('select[name=pathway_level]').val()
        var pathway_tags = $('select[name=pathway_tags]').val()

        // join tags
        pathway_tags = pathway_tags.join()

        // create_pathway
        if (pathway_name) {
            create_pathway(pathway_name, pathway_level, pathway_tags);
        }
        return false;
    });
    // AJAX add resource
    $("body").on('click', 'button[name=button_add_resource_submit]', function () {
        // pathway details
        var pathway_id = $('input[name=edit_pathway_id]').val()
        var resource_name = $('input[name=add_resource_name]').val()
        var resource_link = $('input[name=add_resource_link]').val()
        var resource_type = $('select[name=add_resource_type]').val()

        //console.log(pathway_id, resource_name, resource_link, resource_type)

        if (resource_name) {
            add_resource(pathway_id, resource_name, resource_link, resource_type)
        }
        return false;
    });
    // AJAX delete resource
    $("body").on('click', 'button.delete-resource', function () {
        var pathway_id = $(this).attr('data-pathway-id');
        var resource_id = $(this).attr('data-resource-id');

        $.getJSON($SCRIPT_ROOT + '/_delete_resource', {
            pathway_id: pathway_id,
            resource_id: resource_id
        }, function(data) {
            if (data.response == true) {
                notification("Successfully deleted resource.", "error");
                location.reload();
            } else {
                notification("Something went wrong.", "error");
            }
        });
        return false;
    });
    // AJAX delete pathway
    // $("body").on('click', 'button[name=button_delete_pathway_submit]', function () {
    //     var button_pathway_id = $(this).attr('data-pathway-id');
    //     var input_pathway_id = $('input[name=edit_pathway_id]').val()

    //     if (button_pathway_id == input_pathway_id) {
    //         console.log(button_pathway_id);
    //     }

    //     // $.getJSON($SCRIPT_ROOT + '/_delete_pathway', {
    //     //     pathway_id: pathway_id
    //     // }, function(data) {
    //     //     if (data.response == true) {
    //     //         notification("Successfully deleted pathway.", "error");
    //     //         location.reload();
    //     //     } else {
    //     //         notification("Something went wrong.", "error");
    //     //     }
    //     // });
    //     return false;
    // });

    /* modals
    ------------------------------------------------------- */
    // override close modal
    $("body").on('click', 'a.close', function () {
        $('.modal').removeClass('active');
        $('.modal').addClass('fade');
    });
    // open change password modal
    $("body").on('click', '#button_change_password', function () {
        
        $('#modal_change_password').addClass('active');
    });
    // open reset password modal
    $("body").on('click', '#button_reset_password', function () {
        
        $('#modal_reset_password').addClass('active');
    });
    // open delete account modal
    $("body").on('click', '#button_delete_account', function () {
        
        $('#modal_delete_account').addClass('active');
    });
    // open changelog modal
    $("body").on('click', '#button_changelog', function () {
        
        $('#modal_changelog').addClass('active');
    });
    // open create new pathway modal
    $("body").on('click', '#button_create_new_pathway', function () {
        
        $('#modal_create_new_pathway').addClass('active');
    });
    // open edit pathway modal
    $("body").on('click', '#button_edit_pathway', function () {
        var pathway_id = $(this).attr('data-pathway-id');
        var pathway_name = $(this).attr('data-pathway-name');

        // get resources using pathway_id and JSON
        $.getJSON($SCRIPT_ROOT + '/_pathway_resources', {
            pathway_id: pathway_id
        }, function(data) {
            if (data.response) {
                var pathway_resources = data.response;
                $('#resource_wrapper').text(' ')
                $.each(pathway_resources, function(index, value) {
                    $('#resource_wrapper').append("\
                        <div class='column col-4'>\
                            <p class='m-0'>" + value['name'] + "</p>\
                        </div>\
                        <div class='column col-6'>\
                            <a href=" + value['link'] + " target='_blank' class=''>" + value['link'] + "</a>\
                        </div>\
                        <div class='column col-2'>\
                            <button class='btn btn-link btn-block delete-resource tooltip tooltip-left' data-tooltip='Remove resource: " + value['name'] + "' type='submit' data-pathway-id='" + pathway_id + "' data-resource-id='" + value['resource_id'] + "'><i class='fas fa-minus-circle'></i></button>\
                        </div>\
                    ");
                });
            }
        });

        $('input[name=edit_pathway_id]').attr('value', pathway_id);
        $('input[name=edit_pathway_name]').val(pathway_name);
        $('#modal_edit_pathway').addClass('active');
    });
    // open delete pathway modal
    $("body").on('click', 'button[name=button_delete_pathway_submit]', function () {
        var pathway_id = $('input[name=edit_pathway_id]').val();

        $('input[name=delete_pathway_id]').attr('value', pathway_id);
        $('#modal_delete_pathway').addClass('active');
    });

    /* other
    ------------------------------------------------------- */
    // add pathway_id to localstorage
    $("body").on('click', '#button_pin_pathway', function () {
        var pathway_id = $(this).attr('data-pathway-id');

        // get pinned pathways (SEPARATE THIS INTO FUNCTION)
        var pinned_pathways = get_pinned_pathways();

        // update pinned pathways
        if (!pinned_pathways.includes(pathway_id)) {
            pinned_pathways.push(pathway_id);
            $(this).text('Unpin');
            $("#" + pathway_id).addClass('search-ignore');
        } else {
            pinned_pathways.splice(pinned_pathways.indexOf(pathway_id), 1);
            $(this).text('Pin');
            $("#" + pathway_id).removeClass('search-ignore');
        }
        console.log(pinned_pathways)
        localStorage.setItem('pinned_pathways', pinned_pathways);
    });
    // remove account value on delete
    $("body").on('click', 'a.remove-account-detail', function () {
        var account_detail_id = $(this).attr('id');
        $('input[name=' + account_detail_id + ']').val(' ')
    });
    // remove account avatar (set to default) on delete
    $("body").on('click', 'a.remove-account-avatar', function () {
        $.getJSON($SCRIPT_ROOT + '/_account_remove_avatar', {
            //
        }, function(data) {
            if (data.response != false) {
                console.log('Removed avatar.');
                location.reload();
            } else {
                notification("Something went wrong.", "error");
            }
        });
        return false;
    });
    // close notifications
    $("body").on('click', 'a.notification.close', function () {
        
        $(this).closest('div').remove();
    });
    // change text on accordion label
    $("body").on('click', 'label.label-accordion', function() {
        if ($(this).text() == 'View') {
            $(this).text('Hide');
        } else {
            $(this).text('View');
        }
    });
});