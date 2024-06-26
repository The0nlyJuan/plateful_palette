# Generated by Django 3.1.2 on 2024-06-23 09:38

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
            name='Foods',
            fields=[
                ('food_code', models.IntegerField(primary_key=True, serialize=False)),
                ('food_description', models.CharField(max_length=300)),
                ('food_additional_description', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('ingredient_code', models.IntegerField(primary_key=True, serialize=False)),
                ('ingredient_description', models.CharField(max_length=255)),
                ('alcohol', models.FloatField(blank=True, null=True)),
                ('caffeine', models.FloatField(blank=True, null=True)),
                ('calcium', models.FloatField(blank=True, null=True)),
                ('carbohydrate', models.FloatField(blank=True, null=True)),
                ('carotene_alpha', models.FloatField(blank=True, null=True)),
                ('carotene_beta', models.FloatField(blank=True, null=True)),
                ('cholesterol', models.FloatField(blank=True, null=True)),
                ('choline_total', models.FloatField(blank=True, null=True)),
                ('copper', models.FloatField(blank=True, null=True)),
                ('cryptoxanthin_beta', models.FloatField(blank=True, null=True)),
                ('energy', models.FloatField(blank=True, null=True)),
                ('fatty_acids_total_monounsaturated', models.FloatField(blank=True, null=True)),
                ('fatty_acids_total_polyunsaturated', models.FloatField(blank=True, null=True)),
                ('fatty_acids_total_saturated', models.FloatField(blank=True, null=True)),
                ('fiber_total_dietary', models.FloatField(blank=True, null=True)),
                ('folate_DFE', models.FloatField(blank=True, null=True)),
                ('folate_food', models.FloatField(blank=True, null=True)),
                ('folate_total', models.FloatField(blank=True, null=True)),
                ('folic_acid', models.FloatField(blank=True, null=True)),
                ('iron', models.FloatField(blank=True, null=True)),
                ('lutein_zeaxanthin', models.FloatField(blank=True, null=True)),
                ('lycopene', models.FloatField(blank=True, null=True)),
                ('magnesium', models.FloatField(blank=True, null=True)),
                ('niacin', models.FloatField(blank=True, null=True)),
                ('phosphorus', models.FloatField(blank=True, null=True)),
                ('potassium', models.FloatField(blank=True, null=True)),
                ('protein', models.FloatField(blank=True, null=True)),
                ('retinol', models.FloatField(blank=True, null=True)),
                ('riboflavin', models.FloatField(blank=True, null=True)),
                ('selenium', models.FloatField(blank=True, null=True)),
                ('sodium', models.FloatField(blank=True, null=True)),
                ('sugars_total', models.FloatField(blank=True, null=True)),
                ('theobromine', models.FloatField(blank=True, null=True)),
                ('thiamin', models.FloatField(blank=True, null=True)),
                ('total_fat', models.FloatField(blank=True, null=True)),
                ('vitamin_A_RAE', models.FloatField(blank=True, null=True)),
                ('vitamin_B12', models.FloatField(blank=True, null=True)),
                ('vitamin_B12_added', models.FloatField(blank=True, null=True)),
                ('vitamin_B6', models.FloatField(blank=True, null=True)),
                ('vitamin_C', models.FloatField(blank=True, null=True)),
                ('vitamin_D_D2_D3', models.FloatField(blank=True, null=True)),
                ('vitamin_E_alpha_tocopherol', models.FloatField(blank=True, null=True)),
                ('vitamin_E_added', models.FloatField(blank=True, null=True)),
                ('vitamin_K_phylloquinone', models.FloatField(blank=True, null=True)),
                ('water', models.FloatField(blank=True, null=True)),
                ('zinc', models.FloatField(blank=True, null=True)),
                ('fatty_acid_10_0', models.FloatField(blank=True, null=True)),
                ('fatty_acid_12_0', models.FloatField(blank=True, null=True)),
                ('fatty_acid_14_0', models.FloatField(blank=True, null=True)),
                ('fatty_acid_16_0', models.FloatField(blank=True, null=True)),
                ('fatty_acid_16_1', models.FloatField(blank=True, null=True)),
                ('fatty_acid_18_0', models.FloatField(blank=True, null=True)),
                ('fatty_acid_18_1', models.FloatField(blank=True, null=True)),
                ('fatty_acid_18_2', models.FloatField(blank=True, null=True)),
                ('fatty_acid_18_3', models.FloatField(blank=True, null=True)),
                ('fatty_acid_18_4', models.FloatField(blank=True, null=True)),
                ('fatty_acid_20_1', models.FloatField(blank=True, null=True)),
                ('fatty_acid_20_4', models.FloatField(blank=True, null=True)),
                ('fatty_acid_20_5_n3', models.FloatField(blank=True, null=True)),
                ('fatty_acid_22_1', models.FloatField(blank=True, null=True)),
                ('fatty_acid_22_5_n3', models.FloatField(blank=True, null=True)),
                ('fatty_acid_22_6_n3', models.FloatField(blank=True, null=True)),
                ('fatty_acid_4_0', models.FloatField(blank=True, null=True)),
                ('fatty_acid_6_0', models.FloatField(blank=True, null=True)),
                ('fatty_acid_8_0', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.ingredient')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'ingredient')},
            },
        ),
    ]
