from sqlalchemy.orm import Session

from app.models.calculation import Calculation
from app.core.calculation_factory import perform_calculation


def test_create_calculation_and_read_back(db_session: Session):
    # Arrange
    a = 10.0
    b = 5.0
    calc_type = "mul"

    result = perform_calculation(a, b, calc_type)

    calc = Calculation(
        a=a,
        b=b,
        type=calc_type,
        result=result,
    )

    # Act
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    # Assert
    assert calc.id is not None
    assert calc.a == a
    assert calc.b == b
    assert calc.type == calc_type
    assert calc.result == result
