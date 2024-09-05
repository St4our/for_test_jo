#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from db.models import Plan
from db.repositories.base import BaseRepository


class PlanRepository(BaseRepository):
    model = Plan

    @staticmethod
    def generate_dict(plan: Plan) -> dict:
        return {
            'id': plan.id,
            'name': plan.name,
            'plan_month_value': plan.plan_month_value,
            'plan_month': plan.plan_month,
            'fact_month': plan.fact_month,
            'fact_day': plan.fact_day,
            'created': plan.created,
        }
