from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHealthProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('height_cm', models.FloatField()),
                ('weight_kg', models.FloatField()),
                ('activity_level', models.CharField(max_length=20)),
                ('exercise_days', models.PositiveIntegerField(default=0)),
                ('sleep_hours', models.FloatField(default=7)),
                ('sleep_quality', models.CharField(default='average', max_length=20)),
                ('junk_food_frequency', models.CharField(default='medium', max_length=20)),
                ('sugar_intake', models.CharField(default='medium', max_length=20)),
                ('water_liters', models.FloatField(default=2.0)),
                ('stress_level', models.PositiveIntegerField(default=5)),
                ('mood', models.CharField(default='neutral', max_length=20)),
                ('work_hours', models.PositiveIntegerField(default=8)),
                ('smoking', models.BooleanField(default=False)),
                ('alcohol', models.CharField(default='low', max_length=20)),
                ('family_history', models.BooleanField(default=False)),
                ('existing_conditions', models.CharField(blank=True, max_length=255)),
                ('xp_points', models.PositiveIntegerField(default=0)),
                ('streak_days', models.PositiveIntegerField(default=0)),
                ('last_log_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HealthAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('severity', models.CharField(default='medium', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='health.userhealthprofile')),
            ],
        ),
        migrations.CreateModel(
            name='DailyHealthLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_date', models.DateField()),
                ('sleep_hours', models.FloatField(default=7)),
                ('water_liters', models.FloatField(default=2)),
                ('stress_level', models.PositiveIntegerField(default=5)),
                ('steps', models.PositiveIntegerField(default=3000)),
                ('diet_note', models.CharField(blank=True, max_length=255)),
                ('feeling', models.CharField(blank=True, max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='health.userhealthprofile')),
            ],
            options={
                'ordering': ['-log_date'],
                'unique_together': {('profile', 'log_date')},
            },
        ),
    ]
