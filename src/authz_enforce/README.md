# Enforcing Authorization

This module is a proof of concept for explicitly allow-listing views rather than failing open.
    
    @superuser_required
    def super_admin_view(requrest):
        ....
        return response

If we forget the access control decorator above;

    def super_admin_view(requrest):
        ....
        return response

No one can view our super admin view, rather than allowing everyone in.