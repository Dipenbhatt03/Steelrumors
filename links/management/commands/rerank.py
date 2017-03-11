from django.core.management.base import BaseCommand, CommandError
from links.models import Link
import time


class Command(BaseCommand):
    help = 'My custom django management command'
    def rank_all(self):
        for link in Link.with_votes.all():
            link.Set_Scores()

    def show_all(self):
        print "\n".join("%10s %0.2f" % (l.title, l.rank_scores,
                                        ) for l in Link.with_votes.all())
        print "----\n\n\n"

    def handle(self, *args, **options):
        while 1:
            print "---"
            self.rank_all()
            self.show_all()
            time.sleep(5)

        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
