## Required
- [ ] `/project-edit/<id>`
  - [ ] Error checks & messages
  - [ ] Upload 3D model
  - [ ] Show confirmation dialog when deleting a project
- [ ] `/my-profile` and `/profile/<id>`
  - [ ] Show published projects count
- [ ] `/edit-my-profile`
  - [ ] Change name, nickname, contacts, bio
  - [ ] Change avatar
  - [ ] Error checks & messages
  - [ ] Return to "profile" view
  - [ ] Delete an account
  - [ ] Log out
- [ ] `/login`
  - [ ] Error messages
- [ ] `/signup`
  - [ ] Error messages

## Endpoints
**Catalog** app:
- [ ] `/` - Catalog
  - [ ] Rewrite lorem-ipsum text
- [ ] `/project/<id>` - Project details
  - [ ] When generation fails show `Failed` header & scrollable log panel
  - [ ] Make preview panel fill all the vertical space
  - [ ] Add summary (vertex & polygon count, file size)
  - [ ] Change project card's `no-image` placeholder
  - [ ] Add public/private indication if logged in
- [ ] `/project-edit/<id>` - Edit project
  - [ ] Add `@login_required`
  - [ ] Allow users to upload 3D models
  - [ ] Delete associated images on generation error or new image/model upload
  - [ ] Redirect to `project-edit` after save to show `Processing...` message
  - [ ] Create separate `project-delete` view for project deletion
  - [ ] Add *Are you sure?* pop-up when deleting project
- [ ] `/project-create` - Create project
  - [ ] Add `@login_required`
  - [ ] Set new project status to `empty`
**Users** app:
- [ ] `/profile/<id>` - Profile
  - [ ] Show published project count
- [ ] `/my-profile` - User projects & stuff
  - [ ] Add `@login_required`
  - [ ] Join `my-profile.html` with `profile.html`
- [ ] `/edit-my-profile` - Edit user project
  - [ ] Add `@login_required`
  - [ ] Basic functionality
  - [ ] Avatar upload
  - [ ] Account deletion (probably create new URL)
  - [ ] Add *change password* button & form
- [ ] `/signup` - Create new user
  - [ ] First & second name
  - [ ] Error messages
- [ ] `/login` - Log-in
  - [ ] Error messages
- [x] `/logout` - Logout
  - [ ] ignore if not logged in

## Other stuff
- [ ] Add preview thumbnail generation
- [ ] Allow views to somehow retrieve Metashape logs to show error messages
- [ ] Make `GeneratedModel` model instead of `run_photogrammetry_thread`
      which would rerun Metashape on every `save()`? (suggestion)
- [ ] Add vertex & polygon info generation
- [ ] Remove empty stuff from `mush/photogrammetry`
- [ ] Localization
