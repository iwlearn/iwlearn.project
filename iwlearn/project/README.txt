Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


-*- extra stuff goes here -*-
The LegalFW content type
===============================

In this section we are tesing the LegalFW content type by performing
basic operations like adding, updadating and deleting LegalFW content
items.

Adding a new LegalFW content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'LegalFW' and click the 'Add' button to get to the add form.

    >>> browser.getControl('LegalFW').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'LegalFW' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'LegalFW Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'LegalFW' content item to the portal.

Updating an existing LegalFW content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New LegalFW Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New LegalFW Sample' in browser.contents
    True

Removing a/an LegalFW content item
--------------------------------

If we go to the home page, we can see a tab with the 'New LegalFW
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New LegalFW Sample' in browser.contents
    True

Now we are going to delete the 'New LegalFW Sample' object. First we
go to the contents tab and select the 'New LegalFW Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New LegalFW Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New LegalFW
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New LegalFW Sample' in browser.contents
    False

Adding a new LegalFW content item as contributor
------------------------------------------------

Not only site managers are allowed to add LegalFW content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'LegalFW' and click the 'Add' button to get to the add form.

    >>> browser.getControl('LegalFW').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'LegalFW' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'LegalFW Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new LegalFW content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Basin content type
===============================

In this section we are tesing the Basin content type by performing
basic operations like adding, updadating and deleting Basin content
items.

Adding a new Basin content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Basin' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Basin').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Basin' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Basin Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Basin' content item to the portal.

Updating an existing Basin content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Basin Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Basin Sample' in browser.contents
    True

Removing a/an Basin content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Basin
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Basin Sample' in browser.contents
    True

Now we are going to delete the 'New Basin Sample' object. First we
go to the contents tab and select the 'New Basin Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Basin Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Basin
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Basin Sample' in browser.contents
    False

Adding a new Basin content item as contributor
------------------------------------------------

Not only site managers are allowed to add Basin content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Basin' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Basin').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Basin' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Basin Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Basin content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Project content type
===============================

In this section we are tesing the Project content type by performing
basic operations like adding, updadating and deleting Project content
items.

Adding a new Project content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Project' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Project').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Project' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Project Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Project' content item to the portal.

Updating an existing Project content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Project Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Project Sample' in browser.contents
    True

Removing a/an Project content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Project
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Project Sample' in browser.contents
    True

Now we are going to delete the 'New Project Sample' object. First we
go to the contents tab and select the 'New Project Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Project Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Project
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Project Sample' in browser.contents
    False

Adding a new Project content item as contributor
------------------------------------------------

Not only site managers are allowed to add Project content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Project' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Project').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Project' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Project Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Project content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Project Database content type
===============================

In this section we are tesing the Project Database content type by performing
basic operations like adding, updadating and deleting Project Database content
items.

Adding a new Project Database content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Project Database' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Project Database').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Project Database' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Project Database Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Project Database' content item to the portal.

Updating an existing Project Database content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Project Database Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Project Database Sample' in browser.contents
    True

Removing a/an Project Database content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Project Database
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Project Database Sample' in browser.contents
    True

Now we are going to delete the 'New Project Database Sample' object. First we
go to the contents tab and select the 'New Project Database Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Project Database Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Project Database
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Project Database Sample' in browser.contents
    False

Adding a new Project Database content item as contributor
------------------------------------------------

Not only site managers are allowed to add Project Database content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Project Database' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Project Database').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Project Database' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Project Database Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Project Database content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



