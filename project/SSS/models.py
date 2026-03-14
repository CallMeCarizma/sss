from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

class Contractor(models.Model):
    class ContractorChoices(models.TextChoices):
        CLIENT = "client", "клиент"
        BUILDER = "builder", "подрядчик"

    type = models.CharField(choices=ContractorChoices.choices)
    name = models.CharField(verbose_name="контрагент", unique=True)
    phone = models.CharField(null=True, blank=True, verbose_name="номер телефона")

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"


def equipment_passport_path(instance, filename):
    return f'equipment/passports/{instance.id}/{filename}'


class Equipment(models.Model):
    class EquipmentChoices(models.TextChoices):
        BOILER = "boiler", "котел"
        MANOMETER = "manometer", "манометр"
        CGCP = "CGCP", "газорегуляторный пункт шкафной"

    type = models.CharField(choices=EquipmentChoices.choices, verbose_name="тип оборудования")
    name = models.CharField(verbose_name="название", unique=True)
    verification_date = models.DateField(blank=True, null=True, verbose_name="дата поверки")
    passport_scan = models.FileField(upload_to=equipment_passport_path, null=True, blank=True,
                                     verbose_name="скан паспорта")


class Object(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name="contracted_objects")
    is_opo = models.BooleanField(verbose_name="признак ОПО")

    name = models.CharField(verbose_name="наименование ОПО")
    address = models.CharField(verbose_name="адрес")

    responsible_from_client = models.ForeignKey(Contractor, verbose_name="ответственное лицо от заказчика",
                                                on_delete=models.PROTECT, related_name="client_responsible_objects")
    responsible_from_builder = models.ForeignKey(Contractor, verbose_name="ответственное лицо от ССС",
                                                 on_delete=models.PROTECT, related_name="builder_responsible_objects")

    checking_frequency = models.CharField(verbose_name="периодичность объезда")

    equipment = models.ManyToManyField(Equipment, verbose_name="оборудование")

    class Meta:
        verbose_name = "Объект ОПО"
        verbose_name_plural = "Объекты ОПО"

    def __str__(self):
        return self.name


class ObjectRegistration(models.Model):
    object = models.ForeignKey(
        Object,
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    reg_number = models.CharField(
        verbose_name="Регистрационный номер ОПО"
    )

    issued_at = models.DateField(
        null=True, blank=True,
        verbose_name="Дата регистрации"
    )

    is_active = models.BooleanField(default=True)


class Document(models.Model):
    class DocumentChoices(models.TextChoices):
        AGREEMENT = "agreement", "договор"
        ADDITIONAL_AGREEMENT = "additional_agreement", "доп. соглашение"
        INVOICE = "invoice", "счет на оплату"
        PROJECT = "project", "проект"
        REGISTRATION_CERTIFICATE = "registration_certificate", "свидетельство о регистрации"

    object = models.ForeignKey(Object, on_delete=models.PROTECT, verbose_name="объект")
    type = models.CharField(max_length=100, verbose_name="тип документа", choices=DocumentChoices.choices)
    number = models.BigIntegerField(verbose_name="номер счета в бухгалтерской программе", null=True, blank=True)

    monthly = models.DecimalField(max_digits=15,
                                  decimal_places=2,
                                  validators=[MinValueValidator(Decimal("0.00"))],
                                  verbose_name="ежемесячные",
                                  null=True,
                                  blank=True,
                                  )
    onetime = models.DecimalField(max_digits=15,
                                  decimal_places=2,
                                  validators=[MinValueValidator(Decimal("0.00"))],
                                  verbose_name="разовые",
                                  null=True,
                                  blank=True
                                  )
    comment = models.TextField(verbose_name="комментарии", null=True, blank=True)
    delivery_method = models.CharField(max_length=100, verbose_name="способ отправки", null=True, blank=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return f"Документ {self.pk}"
