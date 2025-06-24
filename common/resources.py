
from import_export import resources, fields
from .models import EducationPlace, City
from import_export.widgets import ForeignKeyWidget

class EducationPlaceResource(resources.ModelResource):
    city = fields.Field(
        attribute='city',
        column_name='Город (ID)',
        widget=ForeignKeyWidget(City, 'name')
    )

    name = fields.Field(attribute='name', column_name='Название ВУЗа')
    link = fields.Field(attribute='link', column_name='Ссылка на сайт')
    rating = fields.Field(attribute='rating', column_name='Рейтинг')
    foundation_date = fields.Field(attribute='foundation_date', column_name='Дата основания')
    is_for_admission = fields.Field(attribute='is_for_admission', column_name='Доступен для поступления')

    class Meta:
        model = EducationPlace
        fields = ('city', 'name', 'link', 'rating', 'foundation_date', 'is_for_admission')
        import_id_fields = ('name',)