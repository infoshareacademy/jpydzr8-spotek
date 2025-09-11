from django.apps import AppConfig
import logging

class AwizacjeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'awizacje'

    def ready(self):
        # Podłącz eksport CSV po zapisie/usunięciu Delivery
        from django.db.models.signals import post_save, post_delete
        from .models import Delivery
        from .utils import export_csv

        logger = logging.getLogger(__name__)

        def _export_after_change(sender, instance, **kwargs):
            try:
                export_csv()  # zapisze do archive/pre-advice.csv
            except Exception:
                logger.exception("CSV export failed")

        post_save.connect(
            _export_after_change, sender=Delivery,
            dispatch_uid="awizacje__export_after_save"
        )
        post_delete.connect(
            _export_after_change, sender=Delivery,
            dispatch_uid="awizacje__export_after_delete"
        )
