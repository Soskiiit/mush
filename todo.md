## Endpoints
**Catalog** app:
- [ ] `/` - Catalog
  - [ ] Rewrite lorem-ipsum text
- [ ] `/project/<id>` - Project details
  - [ ] Make preview panel fill all the vertical space
  - [ ] Add summary (vertex & polygon count, file size)
  - [ ] Change project card's `no-image` placeholder
  - [ ] Add public/private indication if logged in
- [ ] `/project-edit/<id>` - Edit project
  - [ ] Add `@login_required`
  - [ ] When generation fails show `Failed` header & scrollable log panel
  - [ ] Allow users to upload 3D models
  - [ ] Delete associated images on error
  - [ ] Redirect to `project-edit` after save to show `Processing...` message
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
- [ ] Add vertex & polygon info generation
- [ ] Localization
