from optparse import make_option

from django.core.management.base import BaseCommand

from whitelist_auth.models import Whitelisted


class Command(BaseCommand):
    help = 'Show and manage whitelisted users'

    option_list = BaseCommand.option_list + (
        make_option('-a', '--add', action='store_true',
                    help='Add users to whitelist'),
        make_option('--add-admin', action='store_true',
                    help='Add admin users to whitelist'),
        make_option('--remove', action='store_true',
                    help='Remove user from whitelist'),
        make_option('--set-staff', action='store_true',
                    help='Set is_staff=True for users'),
        make_option('--unset-staff', action='store_false', dest='set_staff',
                    help='Set is_staff=False for users'),
        make_option('--set-super', action='store_true',
                    help='Set is_superuser=True for users'),
        make_option('--unset-super', action='store_false', dest='set_super',
                    help='Set is_superuser=False for users'),
        make_option('-l', '--list', action='store_true',
                    help='List whitelisted users'),
    )

    def handle(self, *args, **options):
        def default_action():
            self.print_whitelisted()

        if options['list']:
            default_action()
        elif options['remove']:
            self.remove_whitelisted(*args)
        elif options['add']:
            self.add_whitelisted(*args)
        elif options['add_admin']:
            self.add_admin(*args)
        elif options['set_staff'] is not None:
            self.set_staff(options['set_staff'], *args)
        elif options['set_super'] is not None:
            self.set_super(options['set_super'], *args)
        else:
            default_action()

    def println(self, *args):
        self.stdout.write(' '.join(args))

    def title(self, *args):
        self.println('#', *args)

    def msg(self, *args):
        self.println('*', *args)

    def print_whitelisted(self):
        self.title('whitelisted users')
        for w in Whitelisted.objects.all():
            self.println(w.summary())

    def add_whitelisted(self, *args):
        for email in args:
            try:
                Whitelisted.objects.get(email=email)
            except Whitelisted.DoesNotExist:
                self.msg('adding', email)
                w = Whitelisted(email=email)
                w.save()

    def add_admin(self, *args):
        for email in args:
            try:
                w = Whitelisted.objects.get(email=email)
                w.is_active = True
                w.is_staff = True
                w.is_superuser = True
                self.msg('updated admin:', w.summary())
            except Whitelisted.DoesNotExist:
                self.msg('adding admin user', email)
                w = Whitelisted(email=email, is_staff=True, is_superuser=True)
                w.save()

    def remove_whitelisted(self, *args):
        for email in args:
            self.msg('removing', email)
            w = Whitelisted.objects.get(email=email)
            w.delete()

    def set_staff(self, value, *args):
        for email in args:
            self.msg('setting is_staff=%s for' % value, email)
            w = Whitelisted.objects.get(email=email)
            w.is_staff = value
            w.save()
            self.msg('done:', w.summary())

    def set_super(self, value, *args):
        for email in args:
            self.msg('setting is_superuser=%s for' % value, email)
            w = Whitelisted.objects.get(email=email)
            w.is_superuser = value
            w.save()
            self.msg('done:', w.summary())
