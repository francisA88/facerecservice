# Generated by Django 4.2.4 on 2024-12-02 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_passkey_refimage_delete_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="refimage",
            old_name="image_content",
            new_name="image",
        ),
    ]
