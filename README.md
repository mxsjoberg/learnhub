# LearnHub.io

# TODO

## Prio
    
    [ ] Add social share button to profile page (MAKE SURE META IMAGES WORK FIRST)
    [ ] Route and page for individual pathways (/pathways/<pathway_id>), use explore as search and preview only, use this page for editing (to avoid reloading after adding resource etc.)
    [ ] Delete user-created pathways on account deletion (or remove from owners if multiple) (ADD IMUTABLE ID TO USERS FIRST)
    [ ] Update username in pathways when changing username (ADD IMMUTABLE ID TO USERS FIRST)

## Base

    [X] Button to remove avatar (set to default)
    [X] Button to remove user details
    [X] Delete account
    [X] Reset password

### +++
    
    [X] Upload avatar not working (URI too long?)

## Create pathways

    [X] Create pathway
    [X] Add pathway resource
    [X] Delete pathway resource
    [X] Render pathway resource in edit view
    [ ] Delete pathway

### +++
    
    [ ] Edit pathway details
    [ ] Validate pathway form inputs (no special characters etc.)

## Explore pathways

    [X] Explore page
    [X] Filter search
    [X] Render pathways

### +++

    [X] Pin pathway to top (bookmark): Add button to get pathway_id and add to localstorage, then each load get pathways from localstorage first.

## Projects

    [X] Add project
    [X] Link project with added skills
    [X] Delete project

### +++

    [ ] Edit project details
    [ ] Validate project form inputs (no special characters etc.)

## Presentation

    [X] Create landing page with mockup profile and action buttons (see Doolio.co)

## Other

    [X] Add Google Analytics
    [ ] Transform explore page into "learning hub", search pathways, select pathways, and follow-up on progress etc. (interactive)
    [ ] Add guard for database connection (if no internet or otherwise)

### +++
    
    [-] Revise responsive design (all pages)
    [ ] Control modal open with data-tag
    [ ] Replace non-unique element-ID with data-tag (errorprone with jquery)
