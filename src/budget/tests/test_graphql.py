import json

from django.contrib.auth.models import User
from graphene_django.utils.testing import graphql_query
import pytest

from budget.models import Budget


@pytest.fixture
def user1_client(client):
    user = User.objects.get(username='user1')
    client.force_login(user)
    return client


@pytest.fixture
def user2_client(client):
    user = User.objects.get(username='user2')
    client.force_login(user)
    return client


@pytest.mark.django_db
def test_all_budgets_query(user1_client):
    response = graphql_query(
        '''
        {
            allBudgets {
                id
                name
                created
                updated
                budgetEntries{
                    amount
                }
            }
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert len(content['data']['allBudgets']) == 1


@pytest.mark.django_db
def test_budget_total_query(user1_client):
    response = graphql_query(
        '''
        {
            budgetTotal(budgetId: 6)
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['budgetTotal'] == '5333.00'


@pytest.mark.django_db
def test_budget_total_invalid_id_query(user1_client):
    response = graphql_query(
        '''
        {
            budgetTotal(budgetId: 999)
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['budgetTotal'] is None


@pytest.mark.django_db
def test_all_shared_budgets_query(user2_client):
    response = graphql_query(
        '''
        {
            allSharedBudgets {
                id
                name
                created
                updated
                budgetEntries{
                    amount
                }
            }
        }
        ''',
        client=user2_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert len(content['data']['allSharedBudgets']) == 2


@pytest.mark.django_db
def test_all_budget_entry_categories_query(user1_client):
    response = graphql_query(
        '''
        {
            allBudgetEntryCategories {
                id
                name
            }
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert len(content['data']['allBudgetEntryCategories']) == 3


@pytest.mark.django_db
def test_all_budget_create_query(user1_client):
    response = graphql_query(
        '''
        mutation {
            createBudget (name: "Test bg", sharedWithUsers:[2,3,4]) {
                budget {
                    id
                    name
                }
            }
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content

    pk = content['data']['createBudget']['budget']['id']
    budget = Budget.objects.get(pk=pk)
    assert budget.name == "Test bg"
    assert budget.shared_with_users.all().count() == 3


@pytest.mark.django_db
def test_budget_delete(user1_client):
    response = graphql_query(
        '''
        mutation {
            deleteBudget (id: 3) {
                budget {
                    name
                }
            }
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['deleteBudget'] is not None


@pytest.mark.django_db
def test_budget_delete_not_owned_by_user(user1_client):
    response = graphql_query(
        '''
        mutation {
            deleteBudget (id: 5) {
                budget {
                    name
                }
            }
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['deleteBudget'] is None


@pytest.mark.django_db
def test_budget_delete_invalid_id(user1_client):
    response = graphql_query(
        '''
        mutation {
            deleteBudget (id: 999) {
                budget {
                    name
                }
            }
        }
        ''',
        client=user1_client,
        graphql_url='/graph'
    )

    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['deleteBudget'] is None
