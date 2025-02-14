from factory import Faker, SubFactory, fuzzy, post_generation
from factory.django import DjangoModelFactory

from events.tests.factories import UserFactory
from joboffers.models import Experience, HiringType, JobOffer, Remoteness
from pycompanies.tests.factories import CompanyFactory


class JobOfferFactory(DjangoModelFactory):
    class Meta:
        model = JobOffer

    title = Faker('job')
    company = SubFactory(CompanyFactory)
    location = Faker('address')
    contact_mail = Faker('email')
    contact_phone = Faker('phone_number')
    contact_url = Faker('url')
    experience = fuzzy.FuzzyChoice(Experience.values)
    remoteness = fuzzy.FuzzyChoice(Remoteness.values)
    # tags
    hiring_type = fuzzy.FuzzyChoice(HiringType.values)
    salary = Faker('pricetag')
    description = Faker('paragraph')

    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)

    @post_generation
    def set_created(obj, create, extracted, **kwargs):
        """
        Update the creation time of the built instance. As it is an auto-generated field, we must
        set its value after creation.

        To use: JobFactory(set_created='1985-10-26 09:00Z')

        """
        if extracted:
            obj.created = extracted
            obj.save()
